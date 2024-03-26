from django.db.models import QuerySet
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.views import generic as views

from reviewee_app.place.helpers import find_place_object_by_slug
from reviewee_app.place.models import Restaurant, Hotel
from reviewee_app.review.models import Review, RestaurantReview, HotelReview


# TODO: Got the slug from the place, so we can attach the review to the place object.
# Convention Model-Action-View
# Review/write/place_slug
def place_review_write(request, place_slug):
    return render(request, 'review/review-write.html')


class ReviewWriteView(views.CreateView):

    template_name = 'review/review-write.html'
    available_place_review_types = {
        'Restaurant': RestaurantReview,
        'Hotel': HotelReview,
    }
    slug_url_kwarg = 'place_slug'
    place = None

    def get_form_class(self, **kwargs):
        self.get_place(**kwargs)
        model_class = self.available_place_review_types[self.place.type()]
        return modelform_factory(model_class, fields='__all__')
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        if self.place.type() == 'Restaurant':
            instance.restaurant = self.place
        else:
            instance.hotel = self.place
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        initial['hotel'] = self.place
        return initial
    
    def post(self, request, *args, **kwargs):
        self.get_initial()
        return super().post(request, *args, **kwargs)
    def form_invalid(self, form):
        a = 1
        return super().form_invalid(form)

    def get_place(self):

        place = find_place_object_by_slug(self.kwargs['place_slug'])
        self.place = place
        if not place:
            raise Http404('Place not found')
        return place

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place'] = self.place
        return context

    def get_success_url(self):
        return reverse('place details', kwargs={'slug': self.place.slug})


# TODO: The slug is from the place, the pk is from the review.
def place_review_edit(request, slug, pk):
    return HttpResponse('<h1> Place review edit </h1>')


# Same here, slug is from the place the pk is from the review.
def place_review_delete(request, slug, pk):
    return HttpResponse('<h1> Place review Delete <h/1>')