import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewee_app.settings")
django.setup()


# From here down
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import requests
from reviewee_app.place.models import Hotel


hotel = Hotel.objects.all().first()
review = hotel.reviews.all().first()

user = review.user

print(user.hotelreview_set.all())