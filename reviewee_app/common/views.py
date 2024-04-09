from django.db.models import QuerySet
from django.views import generic as views
from django.shortcuts import Http404

from reviewee_app.favourite.helpers import get_users_favourite_places
from reviewee_app.place.helpers import get_all_places, get_place_by_type, filter_places
from reviewee_app.place.models import Restaurant, Hotel


class HomePageView(views.ListView):

    MAX_PLACES_DISPLAYED = 6
    COUNT_PER_PLACE_TYPE = MAX_PLACES_DISPLAYED / 2
    template_name = 'common/index.html'

    def get_queryset(self):
        object_set = get_all_places((Restaurant, Hotel), count_per_place=self.COUNT_PER_PLACE_TYPE)
        object_set = self.order_queryset_list_by_created_at(object_set)
        return object_set[:self.MAX_PLACES_DISPLAYED]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['users_favourites'] = get_users_favourite_places(self.request.user)
        a = 1
        return context

    @staticmethod
    def order_queryset_list_by_created_at(queryset_list: list):
        return sorted(queryset_list, key=lambda item: item.created_at, reverse=True)


class BrowsePageView(views.ListView):
    template_name = 'common/browse.html'
    paginate_by = 4

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

        except Exception:
            raise Http404('No such place type')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['place'] = self.request.GET.get('place', 0)
        self.auto_fill_search_form_in_context(context)
        context['get_parameters'] = self.paginator_href_builder(context)
        context['users_favourites'] = get_users_favourite_places(self.request.user)
        return context

    def auto_fill_search_form_in_context(self, context):
        context['search'] = self.request.GET.get('search', '')
        context['order'] = self.request.GET.get('order', '')
        return context

    @staticmethod
    def paginator_href_builder(context):
        get_parameters = f"&place={context['place']}"

        if context['search'] != '':
            get_parameters += f"&search={context['search']}"

        if context['order'] != '':
            get_parameters += f"&order={context['order']}"

        return get_parameters
