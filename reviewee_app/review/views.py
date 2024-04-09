from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic as views

from reviewee_app.place.mixins import OwnerOfPlaceCannotCommentMixin
from reviewee_app.review.mixins import ReviewAttachPlaceMixin, ReviewOwnerRequiredMixin
from reviewee_app.review.models import HotelReview, RestaurantReview


# Convention Model-Action-View

class ReviewWriteView(OwnerOfPlaceCannotCommentMixin, ReviewAttachPlaceMixin, LoginRequiredMixin, views.CreateView):

    template_name = 'review/review-write.html'

    def get_form_class(self, **kwargs):
        self.get_place()
        model_class = self.available_place_review_types[self.place.type()]
        return modelform_factory(model_class, fields='__all__')

    def form_valid(self, form):

        previous_review = self.available_place_review_types[self.place.type()].objects.filter(user=self.request.user)
        if previous_review.exists():
            previous_review.delete()

        instance = form.save(commit=False)
        # mega abstraction
        setattr(instance, self.place.type().lower(), self.place)

        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        initial['hotel'] = self.place
        return initial

    def get_success_url(self):
        return reverse('place details', kwargs={'slug': self.place.slug})


# The slug is from the place, the pk is from the review.
class ReviewEditView(ReviewOwnerRequiredMixin, views.UpdateView):

    template_name = 'review/review-edit.html'
    pk_url_kwarg = 'id'

    def get_form_class(self):
        model_class = self.available_place_review_types[self.place.type()]
        return modelform_factory(model_class, fields='__all__')

    def get_queryset(self):
        place = self.get_place()
        queryset = self.available_place_review_types[place.type()].objects.all()
        return queryset

    def get_success_url(self):
        return reverse('place details', kwargs={'slug': self.kwargs['place_slug']})


class ReviewDeleteView(ReviewOwnerRequiredMixin, views.DeleteView):

    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        self.place = self.get_place()
        review = (self.available_place_review_types[self.place.type()]
                  .objects.get(pk=self.kwargs[self.pk_url_kwarg]))
        return review

    def get_success_url(self):
        return reverse('place details', kwargs={'slug': self.kwargs['place_slug']})


class ReviewLike(views.View):

    available_review_types = {
        'HotelReview': HotelReview,
        'RestaurantReview': RestaurantReview,
    }

    def find_review_by_type(self, review_type, review_pk):
        review = self.available_review_types[review_type].objects.get(pk=review_pk)
        return review

    @staticmethod
    def like_functionality(review, user):
        like_instance = review.likes.filter(user=user)

        if like_instance.exists():
            like_instance.delete()
        else:
            if review.type() == 'HotelReview':
                review.likes.create(hotel_review=review, user=user)
            else:
                review.likes.create(restaurant_review=review, user=user)
        return

    def get(self, *args, **kwargs):
        review = self.find_review_by_type(self.kwargs['review_type'], self.kwargs['review_pk'])
        self.like_functionality(review, self.request.user)
        return redirect(self.request.META['HTTP_REFERER'] + f'#{review.pk}')
