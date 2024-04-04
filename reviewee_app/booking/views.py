from datetime import timedelta
from itertools import chain

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.views import generic as views
from django.utils import timezone

from .models import RestaurantBooking, HotelBooking
from ..place.helpers import find_place_object_by_slug
from ..place.models import Restaurant, Hotel
from django.db.models import Case, When, Value


def update_active_bookings(bookings):

    """
    Checks whether the booking date is in the past or the booking is cancelled and if it is, updates the active to False
    :param bookings: QuerySet
    :return: None
    """

    bookings.update(
        active=Case(
            When(Q(date__lt=timezone.localdate()) | Q(canceled=True), then=Value(False)),
            default=Value(True)
        )
    )

    return


def order_bookings(bookings, order_by):

    """
    Created the functions to optimize the ordering process.
    :param bookings: list
    :param order_by: str
    :return: list
    """

    def order_by_created_at_desc():
        return list(sorted(bookings, reverse=True, key=lambda x: x.date))

    def order_by_created_asc():
        return list(sorted(bookings, key=lambda x: x.date))

    options = {
        '-date': order_by_created_at_desc,
        'date': order_by_created_asc,
    }

    if order_by in options:
        return options[order_by]()

    return bookings


def find_all_bookings_from_search_data(search: str, option: str, order_by='-date'):

    if search is None:
        return []

    options = {
        'active': Q(active=True),
        'inactive': Q(active=False),
    }

    if option in options:
        query = (Q(email__iexact=search) | Q(confirmation_code__exact=search)) & options[option]
    else:
        query = Q(email__iexact=search) | Q(confirmation_code__exact=search)

    restaurant_bookings = RestaurantBooking.objects.filter(query)
    hotel_bookings = HotelBooking.objects.filter(query)

    for bookings in (restaurant_bookings, hotel_bookings):
        update_active_bookings(bookings)

    all_bookings = list(chain(restaurant_bookings, hotel_bookings))
    all_bookings = order_bookings(all_bookings, order_by)

    return all_bookings


class BookingOwnerRequiredMixin(AccessMixin):

    @staticmethod
    def booking_ownership_verified(request, **kwargs):
        return kwargs['slug'] in request.session['owned_bookings']

    def dispatch(self, request, *args, **kwargs):

        if self.booking_ownership_verified(request, **kwargs):
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class BookingVeryfiOwnershipView(views.DetailView):
    template_name = 'booking/booking-verify-ownership.html'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        if 'restaurant' in self.kwargs['slug'].lower():
            return RestaurantBooking.objects.all()
        return HotelBooking.objects.all()
    
    def post(self, request, **kwargs):
        users_input = self.request.POST.get('code', '')
        self.object = self.get_object()
        a = 1
        if users_input == self.object.confirmation_code:
            session_data = request.session.get('owned_bookings', [])
            session_data.append(self.object.slug) if self.object.slug not in session_data else session_data
            request.session['owned_bookings'] = session_data
            return redirect('manage booking', **self.kwargs)

        return self.get(request, **kwargs)


class BookingManageView(BookingOwnerRequiredMixin, views.UpdateView):

    template_name = 'booking/booking-manage.html'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        if 'restaurant' in self.kwargs['slug'].lower():
            return RestaurantBooking.objects.all()
        return HotelBooking.objects.all()

    def get_form_class(self):
        if'restaurant' in self.kwargs['slug'].lower():
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
        if hasattr(self.object, 'hotel'):
            context['night_range'] = range(HotelBooking.MIN_NIGHTS_PER_BOOKING, HotelBooking.MAX_NIGHTS_PER_BOOKING + 1)
            context['rooms_range'] = range(HotelBooking.MIN_ROOMS_PER_BOOKING, HotelBooking.MAX_ROOMS_PER_BOOKING + 1)
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


class BookingConfirmationDataInSessionMixin:

    @staticmethod
    def attach_booking_info_to_session(request, booking):
        if hasattr(booking, 'restaurant'):
            request.session['place_name'] = booking.restaurant.name
        else:
            request.session['place_name'] = booking.hotel.name
        request.session['date'] = str(booking.date)
        request.session['confirmation_code'] = booking.confirmation_code
        request.session['email'] = booking.email


class BookingBookRestaurantView(BookingConfirmationDataInSessionMixin ,views.CreateView):

    template_name = 'booking/book-restaurant.html'
    restaurant = None

    def get_form_class(self):
        return modelform_factory(RestaurantBooking, exclude=['canceled', 'active'])

    def get_success_url(self):
        return reverse('booking successful')

    def form_valid(self, form):
        instance = form.save()
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
            self.restaurant = Restaurant.objects.get(slug=self.kwargs['place_slug'])
            # TODO: if not restaurant found by the slug, raise 404
        return self.restaurant


class BookingBookHotel(BookingConfirmationDataInSessionMixin, views.CreateView):
    template_name = 'booking/book-hotel.html'
    hotel = None

    def get_form_class(self):
        return modelform_factory(HotelBooking, exclude=['canceled', 'active'])

    def get_success_url(self):
        return reverse('booking successful')

    def form_valid(self, form):
        instance = form.save()
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
            self.hotel = Hotel.objects.get(slug=self.kwargs['place_slug'])
            # TODO: if not hotel found by the slug, raise 404
        return self.hotel


class BookingSuccessfulView(views.TemplateView):
    template_name = 'booking/booking-successful.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place_name'] = self.request.session['place_name']
        context['email'] = self.request.session['email']
        context['date'] = self.request.session['date']
        context['confirmation_code'] = self.request.session['confirmation_code']
        # context['place_name'] = self.request.session.pop('place_name')
        # context['email'] = self.request.session.pop('email')
        # context['date'] = self.request.session.pop('date')
        # context['confirmation_code'] = self.request.session.pop('confirmation_code')
        return context


def book_place(request, slug):  # place slug
    return HttpResponse('Book Place Page')


def booking_all(request):
    return HttpResponse('All My Bookings Page')


def booking_details(request, pk):
    return HttpResponse('Booking Details Page')


def booking_cancel(request, pk):
    return HttpResponse('Booking Cancel Page')
