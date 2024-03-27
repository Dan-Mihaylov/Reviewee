from django.db.models import QuerySet
from django.forms import modelform_factory
from django.urls import reverse
from django.views import generic as views

from reviewee_app.review.mixins import ReviewAttachPlaceMixin, ReviewOwnerRequiredMixin


# TODO: Got the slug from the place, so we can attach the review to the place object.
# Convention Model-Action-View
# Review/write/place_slug

class ReviewWriteView(ReviewAttachPlaceMixin, views.CreateView):

    template_name = 'review/review-write.html'

    def get_form_class(self, **kwargs):
        self.get_place(**kwargs)
        model_class = self.available_place_review_types[self.place.type()]
        return modelform_factory(model_class, fields='__all__')

    def form_valid(self, form):
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


# TODO: The slug is from the place, the pk is from the review.
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
