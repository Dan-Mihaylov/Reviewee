from .models import Restaurant, Hotel


# Because we have a few place models and DRY
def find_place_object_for_user(user, slug):
    if user.restaurants.filter(slug=slug).exists():
        return user.restaurants.get(slug=slug)
    else:
        return user.hotels.get(slug=slug)


def find_place_object_by_slug(slug):
    if Restaurant.objects.filter(slug=slug).prefetch_related('reviews').exists():
        return Restaurant.objects.get(slug=slug)
    elif Hotel.objects.filter(slug=slug).prefetch_related('reviews').exists():
        return Hotel.objects.get(slug=slug)


def get_all_photo_reviews(object):
    return [review for review in object.reviews.all() if review.review_photo]