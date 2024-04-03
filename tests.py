import os
import random

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewee_app.settings")
django.setup()


# From here down
from django.contrib.auth import get_user_model
from reviewee_app.favourite.helpers import get_users_favourite_places
from django.core.exceptions import ValidationError
import requests
from reviewee_app.place.models import Hotel, Restaurant
from reviewee_app.place.helpers import get_all_places, get_place_by_type
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from reviewee_app.booking.helpers import generate_random_confirmation_code



# restaurants = get_all_restaurants()
#
# restaurants_with_ratings = Restaurant.objects.annotate(
#     avg_rating=Coalesce(
#         Avg('reviews__rating'),
#         Value(0),
#         output_field=FloatField(),
#     )
# )
#
# for restaurant in restaurants_with_ratings:
#     print(restaurant.avg_rating)
# UserModel = get_user_model()
# user = UserModel.objects.get(pk=38)
#
# favourite_places = get_users_favourite_places(user)
# print(favourite_places)
#
# for place in favourite_places:
#     print(place.created_at)

print(generate_random_password(6))