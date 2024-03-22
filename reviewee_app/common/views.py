from django.shortcuts import render, HttpResponse
from django.views import generic as views

from reviewee_app.place.helpers import get_all_places


"""
    Home page will display the 6 last added items, then you have the choice to browse restaurants
    or to browse hotels. This can go into another index or something else page, where we can get 
    the QuerySet and perform filtering and pagination on it. I can't do it on the home page, because
    when I fetch all the places, I return them as list.
"""


# TODO: Convention Model-Action-View
class HomePageView(views.ListView):

    MAX_PLACES_DISPLAYED = 6
    template_name = 'common/index.html'

    def get_queryset(self):
        object_set =  get_all_places()
        object_set = self.order_queryset_list_by_created_at(object_set)
        return object_set[:self.MAX_PLACES_DISPLAYED]

    def order_queryset_list_by_created_at(self, queryset_list: list):
        return sorted(queryset_list, key=lambda item: item.created_at, reverse=True)


class BrowsePageView(views.ListView):
    pass

