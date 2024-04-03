from datetime import timedelta

from django.forms import modelform_factory
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.views import generic as views

from .models import RestaurantBooking, HotelBooking
from ..place.helpers import find_place_object_by_slug
from ..place.models import Restaurant


class BookingFindView(views.TemplateView):
    pass


class BookingBookRestaurantView(views.CreateView):

    template_name = 'booking/book-restaurant.html'
    restaurant = None

    def get_form_class(self):
        return modelform_factory(RestaurantBooking, exclude=['canceled'])

    def get_success_url(self):
        return reverse('booking successful')

    def form_valid(self, form):
        instance = form.save()
        self.request.session['place_name'] = instance.restaurant.name
        self.request.session['date'] = str(instance.date)
        self.request.session['confirmation_code'] = instance.confirmation_code
        self.request.session['email'] = instance.email
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        self.get_restaurant()
        initial['restaurant'] = self.restaurant
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place_slug'] = self.restaurant.slug
        context['restaurant_times'] = {
            'opening_time': self.restaurant.opening_time.strftime('%H:%M'),
            'closing_time': self.restaurant.closing_time.replace(hour=(self.restaurant.closing_time.hour - 1)
                                                                 ).strftime('%H:%M'),
        }
        return context

    def get_restaurant(self):
        if not self.restaurant:
            self.restaurant = Restaurant.objects.get(slug=self.kwargs['place_slug'])
        return self.restaurant


class BookingSuccessfulView(views.TemplateView):
    template_name = 'booking/booking-successful.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place_name'] = self.request.session.pop('place_name')
        context['email'] = self.request.session.pop('email')
        context['date'] = self.request.session.pop('date')
        context['confirmation_code'] = self.request.session.pop('confirmation_code')
        return context

def book_place(request, slug):  # place slug
    return HttpResponse('Book Place Page')


def booking_all(request):
    return HttpResponse('All My Bookings Page')


def booking_details(request, pk):
    return HttpResponse('Booking Details Page')


def booking_cancel(request, pk):
    return HttpResponse('Booking Cancel Page')

