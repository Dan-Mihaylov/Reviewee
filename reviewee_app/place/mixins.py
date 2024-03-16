from django.contrib.auth.mixins import AccessMixin
from reviewee_app.account.mixins import BusinessOwnerRequiredMixin


class OwnerOfPlaceRequiredMixin(BusinessOwnerRequiredMixin):

    def check_if_place_in_places(self):
        try:
            # getting errors from anonymous users for attribute
            restaurants_queryset = self.request.user.restaurants.filter(slug=self.kwargs['slug'])
            hotels_queryset = self.request.user.hotels.filter(slug=self.kwargs['slug'])

            return restaurants_queryset.exists() or hotels_queryset.exists()

        except AttributeError:
            return False

    def dispatch(self, request, *args, **kwargs):

        result = super().dispatch(request, *args, **kwargs)

        if self.check_if_place_in_places():
            return result

        return self.handle_no_permission()