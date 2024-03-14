from django.forms import modelform_factory
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.views import generic as views

from .models import BasePlaceModel, Restaurant, Hotel
from ..account.mixins import BusinessOwnerRequiredMixin


# TODO: Convention Model-Action-View
class PlaceAddView(BusinessOwnerRequiredMixin, views.TemplateView):
    template_name = 'place/place-add.html'


class RestaurantAddView(views.CreateView):
    template_name = 'place/restaurant-add.html'
    form_class = modelform_factory(Restaurant, fields='__all__')

    # TODO: add the user automatically, don't select it.
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return super().form_valid(form)
    def get_success_url(self):
        # you get the object in the form_valid() in the CreateView
        return reverse('home')


class HotelAddView(views.CreateView):
    template_name = 'place/hotel-add.html'
    form_class = modelform_factory(Hotel, fields='__all__')

    # TODO: Add the user automatically, remove the field from the form
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


def place_details(request, slug):
    return HttpResponse('Place Details Page')


def place_bookings(request, slug):
    return HttpResponse('Place Bookings Page')


def place_edit(request, slug):
    return HttpResponse('Place Edit Page')


def place_delete(request, slug):
    return HttpResponse('Place Delete Page')


def place_review_write(request, slug):
    return HttpResponse('Place Review Write Page')


def place_review_edit(request, slug, pk):
    return HttpResponse('Place Review Edit Page')


def place_review_delete(request, slug, pk):
    return HttpResponse('Place Review Delete Page')
