import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewee_app.settings")
django.setup()


# From here down
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import requests
from reviewee_app.place.models import Hotel, Restaurant
from reviewee_app.place.helpers import get_all_places, get_place_by_type, get_users_favourite_places
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce



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
UserModel = get_user_model()
user = UserModel.objects.get(pk=38)

favourite_places = get_users_favourite_places(user)
print(favourite_places)
