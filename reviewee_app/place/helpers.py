from django.db.models import QuerySet, Avg, Value, FloatField, Q
from django.db.models.functions import Coalesce

from django.contrib.auth import get_user_model

from .models import Restaurant, Hotel, BasePlaceModel
from itertools import chain

UserModel = get_user_model()


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


def order_place(queryset: QuerySet, order_by: str) -> QuerySet:
    ordering = {
        'latest': '-created_at',
        'oldest': 'created_at',
        'highest-rating': '-avg_rating',
        'lowest-rating': 'avg_rating',
    }

    queryset = queryset.order_by(ordering[order_by]) if order_by in ordering else queryset.order_by('-created_at')

    return queryset


# TODO: lvl of abstraction, get place by type...
def get_place_by_type(type_: BasePlaceModel, order_by='latest', count='__all__') -> QuerySet:
    """
    :param type_: Type of Place, Restaurant, Hotel
    :param order_by: str -> one of 'latest', 'oldest', 'highest-rating', 'lowest-rating'
    :param count: Int or '__all__'
    :return: QuerySet
    """

    queryset = (type_.objects
                .prefetch_related('favourite_to_users')
                .prefetch_related('reviews')
                .annotate(
                    avg_rating=Coalesce(
                    Avg('reviews__rating'),
                        Value(0),
                        output_field=FloatField(),
                    )
                )
                )

    queryset = order_place(queryset, order_by)

    if count == '__all__':
        return queryset

    try:
        return queryset[:count]

    except:  # TODO: Make it more specific
        return queryset


def get_all_places(place_types: tuple, order_by='-created_at', count_per_place='__all__') -> list:
    all_places = [get_place_by_type(type_, count=count_per_place) for type_ in place_types]
    result = list(chain(*all_places))

    return result


def filter_places(queryset: QuerySet, filter_parameters: str) -> QuerySet:
    query = Q(name__icontains=filter_parameters) | Q(country__icontains=filter_parameters)

    queryset = queryset.filter(query)
    print('finished filtering')

    return queryset


# Get all the places for the current user and chain them into a list
def get_users_places(pk: int) -> list:
    try:
        user = UserModel.objects.get(pk=pk)
        restaurants = user.restaurants.all()
        hotels = user.hotels.all()
        return list(chain(restaurants, hotels))
    except:
        return []

# TODO: Check whether a place is in users favourite places.


def get_users_favourite_places(user: UserModel) -> list:

    if user.is_authenticated:
        favourite_hotels = [favourite.hotel for favourite in user.favouritehotel_set.all()]
        favourite_restaurants = [favourite.restaurant for favourite in user.favouriterestaurant_set.all()]

        all_favourite_places = list(chain(favourite_hotels, favourite_restaurants))
        return all_favourite_places

    return []
