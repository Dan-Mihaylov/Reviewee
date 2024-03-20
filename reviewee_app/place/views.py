from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelform_factory
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.views import generic as views

from .mixins import OwnerOfPlaceRequiredMixin
from .models import BasePlaceModel, Restaurant, Hotel
from .helpers import find_place_object_for_user, find_place_object_by_slug, get_all_photo_reviews
from ..account.mixins import BusinessOwnerRequiredMixin


# TODO: Convention Model-Action-View
class PlaceAddView(BusinessOwnerRequiredMixin, views.TemplateView):
    template_name = 'place/place-add.html'


class RestaurantAddView(BusinessOwnerRequiredMixin, views.CreateView):
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


class HotelAddView(BusinessOwnerRequiredMixin, views.CreateView):
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


# TODO: make sure you can't change the owner of the place - Done
class PlaceEditView(OwnerOfPlaceRequiredMixin, views.UpdateView):
    template_name = 'place/place-edit.html'

    def get_object(self, queryset=None):
        return find_place_object_for_user(self.request.user, self.kwargs['slug'])
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_form_class(self):
        return modelform_factory(type(self.object), fields='__all__')

    # TODO: Change the redirect URL to the place, details page.
    def get_success_url(self):
        return reverse('home')


class PlaceDeleteView(OwnerOfPlaceRequiredMixin, views.DeleteView):
    template_name = 'place/place-delete.html'

    def get_success_url(self):
        return reverse('home')

    def get_object(self, queryset=None):
        return find_place_object_for_user(self.request.user, self.kwargs['slug'])


# TODO: Finish Place Details, add extra context, book, add review
class PlaceDetailsView(views.DetailView):
    template_name = 'place/place-details.html'

    def get_object(self, queryset=None):
        return find_place_object_by_slug(self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_reviews'] = get_all_photo_reviews(self.object)
        return context


def place_bookings(request, slug):
    return HttpResponse('Place Bookings Page')


def place_review_write(request, slug):
    return HttpResponse('Place Review Write Page')


def place_review_edit(request, slug, pk):
    return HttpResponse('Place Review Edit Page')


def place_review_delete(request, slug, pk):
    return HttpResponse('Place Review Delete Page')
