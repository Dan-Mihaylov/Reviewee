from django.shortcuts import render, HttpResponse, redirect
from django.views import generic as views

from reviewee_app.place.helpers import get_all_places, get_place_by_type, filter_places
from reviewee_app.place.models import Restaurant, Hotel

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
        object_set =  get_all_places((Restaurant, Hotel))
        # object_set = self.order_queryset_list_by_created_at(object_set)
        return object_set[:self.MAX_PLACES_DISPLAYED]

    @staticmethod
    def order_queryset_list_by_created_at(queryset_list: list):
        return sorted(queryset_list, key=lambda item: item.created_at, reverse=True)


class BrowsePageView(views.ListView):
    # TODO: Paginator
    template_name = 'common/browse.html'
    allow_empty = True     # raises 404 if False

    available_place_types = {
        'restaurants': Restaurant,
        'hotels': Hotel,
    }

    def get_queryset(self):

        try:
            place_type = self.request.GET.get('place', '')
            order = self.request.GET.get('order', '')

            queryset = get_place_by_type(
                self.available_place_types[place_type],
                order_by=order,
            )

            if self.request.GET.get('search', '') == '':
                return queryset
            else:
                return filter_places(queryset, self.request.GET.get('search', ''))

        except KeyError:
            return

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['place'] = self.request.GET.get('place', 0)
        context = self.auto_fill_search_form_in_context(context)
        return context

    def auto_fill_search_form_in_context(self, context):
        context['search'] = self.request.GET.get('search', '')
        context['order'] = self.request.GET.get('order', '')
        return context
