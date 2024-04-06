from django.contrib.auth.mixins import AccessMixin
from reviewee_app.account.mixins import BusinessOwnerRequiredMixin
from reviewee_app.place.helpers import find_place_object_by_slug


class OwnerOfPlaceRequiredMixin(BusinessOwnerRequiredMixin):

    def check_place_belongs_to_user(self, request, **kwargs):
        try:
            # getting errors from anonymous users for attribute
            slug = self.find_place_slug(request, **kwargs)
            restaurants_queryset = request.user.restaurants.filter(slug=slug)
            hotels_queryset = request.user.hotels.filter(slug=slug)

            return restaurants_queryset.exists() or hotels_queryset.exists()

        except AttributeError or KeyError:
            return False

    @staticmethod
    def find_place_slug(request, **kwargs):
        slug = kwargs['slug'] if 'slug' in kwargs else request.GET.get('slug', '')
        return slug

    def dispatch(self, request, *args, **kwargs):

        if self.check_place_belongs_to_user(request, **kwargs):
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class OwnerOfPlaceCannotCommentMixin(AccessMixin):

    @staticmethod
    def user_is_the_place_owner(request,  **kwargs):
        place = find_place_object_by_slug(kwargs['place_slug'])
        return request.user == place.owner

    def dispatch(self, request, *args, **kwargs):

        if self.user_is_the_place_owner(request, **kwargs):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
