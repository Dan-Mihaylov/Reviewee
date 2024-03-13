from django.forms import modelform_factory
from django.shortcuts import render, HttpResponse
from django.views import generic as views

from .models import BasePlaceModel
from ..account.mixins import BusinessOwnerRequiredMixin


# TODO: Convention Model-Action-View
class PlaceAddView(BusinessOwnerRequiredMixin, views.TemplateView):
    template_name = 'place/place-add.html'


class RestaurantAddView(views.CreateView):
    pass


class HotelAddView(views.CreateView):
    pass

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
