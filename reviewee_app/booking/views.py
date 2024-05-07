from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import QuerySet
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic as views
from django.http import Http404


from reviewee_app.booking.helpers import find_all_bookings_for_place, find_all_bookings_from_search_data, \
    filter_place_bookings_for_date
from reviewee_app.booking.mixins import BookingOwnerRequiredMixin, BookingConfirmationDataInSessionMixin
from reviewee_app.booking.models import RestaurantBooking, HotelBooking
from reviewee_app.notification.helpers import create_notification_for_place_booking
from reviewee_app.place.helpers import find_place_object_by_slug
from reviewee_app.place.mixins import OwnerOfPlaceRequiredMixin
from reviewee_app.place.models import Restaurant, Hotel


class BookingBookRestaurantView(BookingConfirmationDataInSessionMixin, views.CreateView):

    template_name = 'booking/book-restaurant.html'
    restaurant = None

    def get_form_class(self):
        return modelform_factory(RestaurantBooking, exclude=['canceled', 'active'])

    def get_success_url(self):
        return reverse('booking successful')

    def form_valid(self, form):
        instance = form.save()
        create_notification_for_place_booking(self.restaurant, instance)
        self.attach_booking_info_to_session(self.request, instance)
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        self.get_restaurant()
        initial['restaurant'] = self.restaurant
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place_slug'] = self.restaurant.slug
        context['restaurant'] = self.restaurant
        context['restaurant_times'] = {
            'opening_time': self.restaurant.opening_time.strftime('%H:%M'),
            'closing_time': self.restaurant.closing_time.replace(hour=(self.restaurant.closing_time.hour - 1)
                                                                 ).strftime('%H:%M'),
        }
        return context

    def get_restaurant(self):
        if not self.restaurant:
            try:
                self.restaurant = Restaurant.objects.get(slug=self.kwargs['place_slug'])
                return self.restaurant
            except ObjectDoesNotExist:
                raise Http404('Resource Not Found')
            except MultipleObjectsReturned:
                raise Http404('Multiple Objects Returned')


class BookingBookHotelView(BookingConfirmationDataInSessionMixin, views.CreateView):
    template_name = 'booking/book-hotel.html'
    hotel = None

    def get_form_class(self):
        return modelform_factory(HotelBooking, exclude=['canceled', 'active'])

    def get_success_url(self):
        return reverse('booking successful')

    def form_valid(self, form):
        instance = form.save()
        create_notification_for_place_booking(self.hotel, instance)
        self.attach_booking_info_to_session(self.request, instance)
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        self.get_hotel()
        initial['hotel'] = self.hotel
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place_slug'] = self.hotel.slug
        context['hotel'] = self.hotel
        context['night_range'] = range(HotelBooking.MIN_NIGHTS_PER_BOOKING, HotelBooking.MAX_NIGHTS_PER_BOOKING + 1)
        context['rooms_range'] = range(HotelBooking.MIN_ROOMS_PER_BOOKING, HotelBooking.MAX_ROOMS_PER_BOOKING + 1)
        return context

    def get_hotel(self):
        if not self.hotel:
            try:
                self.hotel = Hotel.objects.get(slug=self.kwargs['place_slug'])
                return self.hotel
            except ObjectDoesNotExist:
                raise Http404('Resource Does Not Exist')
            except MultipleObjectsReturned:
                raise Http404('Multiple Objects Returned')


class BookingSuccessfulView(views.TemplateView):
    template_name = 'booking/booking-successful.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place_name'] = self.request.session['place_name']
        context['email'] = self.request.session['email']
        context['date'] = self.request.session['date']
        context['confirmation_code'] = self.request.session['confirmation_code']
        return context


class BookingFindView(views.ListView):
    template_name = 'booking/find-booking.html'

    def get_queryset(self):
        return find_all_bookings_from_search_data(self.request.GET.get('search'), self.request.GET.get('filter'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['filter'] = self.request.GET.get('filter', '')
        return context


class BookingManageView(BookingOwnerRequiredMixin, views.UpdateView):
    template_name = 'booking/booking-manage.html'
    slug_url_kwarg = 'slug'

    def get_queryset(self):

        if 'restaurant' in self.kwargs['slug'].lower():
            return RestaurantBooking.objects.all()

        return HotelBooking.objects.all()

    def get_form_class(self):

        if 'restaurant' in self.kwargs['slug'].lower():
            return modelform_factory(RestaurantBooking, exclude=['active', 'restaurant'])

        return modelform_factory(HotelBooking, exclude=['active', 'hotel'])

    def form_valid(self, form):
        instance = form.save()
        print(instance.canceled)

        if instance.canceled:
            owned_bookings_list = self.request.session['owned_bookings']
            owned_bookings_list.remove(instance.slug)
            self.request.session['owned_bookings'] = owned_bookings_list
            return HttpResponseRedirect(reverse('home'))

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('manage booking', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place'] = self.object.hotel if hasattr(self.object, 'hotel') else self.object.restaurant

        if hasattr(self.object, 'hotel'):
            context['night_range'] = range(HotelBooking.MIN_NIGHTS_PER_BOOKING, HotelBooking.MAX_NIGHTS_PER_BOOKING + 1)
            context['rooms_range'] = range(HotelBooking.MIN_ROOMS_PER_BOOKING, HotelBooking.MAX_ROOMS_PER_BOOKING + 1)

        return context


class BookingVeryfiOwnershipView(views.DetailView):
    template_name = 'booking/booking-verify-ownership.html'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        if 'restaurant' in self.kwargs['slug'].lower():
            return RestaurantBooking.objects.all()
        return HotelBooking.objects.all()

    def get(self, request, **kwargs):
        session_data = request.session.get('owned_bookings', [])
        self.object = self.get_object()

        if self.object.slug in session_data:
            return redirect('manage booking', **kwargs)

        return super().get(request, **kwargs)
    
    def post(self, request, **kwargs):
        users_input = self.request.POST.get('code', '')
        self.object = self.get_object()

        if users_input == self.object.confirmation_code:
            session_data = request.session.get('owned_bookings', [])
            session_data.append(self.object.slug) if self.object.slug not in session_data else session_data
            request.session['owned_bookings'] = session_data
            return redirect('manage booking', **self.kwargs)

        return self.get(request, **kwargs)


class BookingPlaceBookingsListView(OwnerOfPlaceRequiredMixin, views.ListView):
    template_name = 'booking/booking-place-bookings-list.html'
    paginate_by = 10
    place = None

    def get_queryset(self):
        try:
            self.place = find_place_object_by_slug(self.request.GET.get('slug', ''))
            bookings = find_all_bookings_for_place(
                self.place,
                filter_by=self.request.GET.get('filter_by', 'active'),
                order_by=self.request.GET.get('order_by', ''),
            )
            if self.request.GET.get('for_date', '') != '':
                return filter_place_bookings_for_date(bookings, self.request.GET.get('for_date', ''))

            return bookings

        except Exception:
            return QuerySet

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['place'] = self.place
        context['is_restaurant'] = 'restaurant' in self.request.GET.get('slug', '')
        self.auto_fill_search_form_in_context(context)
        context['get_parameters'] = self.paginator_href_builder(context)
        return context

    def auto_fill_search_form_in_context(self, context):
        context['slug'] = self.request.GET.get('slug', '')
        context['order_by'] = self.request.GET.get('order_by', '')
        context['filter_by'] = self.request.GET.get('filter_by', '')
        context['for_date'] = self.request.GET.get('for_date', '')
        return context

    @staticmethod
    def paginator_href_builder(context):
        get_parameters = f"?slug={context['slug']}"

        if context['order_by'] != '':
            get_parameters += f"&search={context['order_by']}"

        if context['filter_by'] != '':
            get_parameters += f"&order={context['filter_by']}"

        if context['for_date'] != '':
            get_parameters += f"&for_date={context['for_date']}"

        return get_parameters


