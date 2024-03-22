from django.db.models import QuerySet

from .models import Restaurant, Hotel
from itertools import chain


# Because we have a few place models and DRY
def find_place_object_for_user(user, slug) -> Restaurant or Hotel:
    if user.restaurants.filter(slug=slug).exists():
        return user.restaurants.get(slug=slug)
    else:
        return user.hotels.get(slug=slug)


def find_place_object_by_slug(slug) -> Restaurant or Hotel:
    if Restaurant.objects.filter(slug=slug).prefetch_related('reviews').exists():
        return Restaurant.objects.get(slug=slug)
    elif Hotel.objects.filter(slug=slug).prefetch_related('reviews').exists():
        return Hotel.objects.get(slug=slug)


def get_all_photo_reviews(object) -> list:
    return [review for review in object.reviews.all() if review.review_photo]


def get_all_restaurants(order_by='-created-at') -> QuerySet:

    return Restaurant.objects.order_by(order_by)


def get_all_hotels(order_by='-created-at') -> QuerySet:

    return Hotel.objects.order_by(order_by)


def get_all_places(order_by='-created_at') -> list:

    restaurants = get_all_restaurants(order_by)
    hotels = get_all_hotels(order_by)

    all_places = list(chain(restaurants, hotels))

    return all_places