from django.contrib.auth.mixins import AccessMixin
from django.http import Http404

from reviewee_app.place.helpers import find_place_object_by_slug
from reviewee_app.review.models import RestaurantReview, HotelReview


class ReviewAttachPlaceMixin:
    """
    <slug:place_slug> must be passed as a **kwarg through the URL
    Finds the place and attaches it to the context
    """

    place = None
    available_place_review_types = {
        'Restaurant': RestaurantReview,
        'Hotel': HotelReview,
    }

    def get_place(self):

        if self.place is None:
            self.place = find_place_object_by_slug(self.kwargs['place_slug'])
        if not self.place:
            raise Http404('Place not found')
        return self.place

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place'] = self.place
        return context


class ReviewOwnerRequiredMixin(AccessMixin, ReviewAttachPlaceMixin):
    def check_if_user_is_review_owner(self):
        if self.request.user.is_authenticated:
            self.place = self.get_place()
            review = (self.available_place_review_types[self.place.type()]
                      .objects
                      .get(pk=self.kwargs[self.pk_url_kwarg]))
            if review.user.pk == self.request.user.pk:
                return True

        return False

    def dispatch(self, request, *args, **kwargs):

        if self.check_if_user_is_review_owner():
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()