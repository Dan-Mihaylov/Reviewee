from django.contrib.auth import get_user_model
from itertools import chain


UserModel = get_user_model()


def get_users_favourite_places(user: UserModel) -> list:

    # user not authenticated raises
    try:
        fav_restaurants = [fav.restaurant for fav in user.favouriterestaurant_set.all().order_by('-created_at')]
        fav_hotels = [fav.hotel for fav in user.favouritehotel_set.all().order_by('-created_at')]

        favourites = list(chain(fav_restaurants, fav_hotels))

        return favourites

    except AttributeError:
        return []
