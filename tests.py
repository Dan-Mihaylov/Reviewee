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
from reviewee_app.place.helpers import get_all_places



places = get_all_places()

# for place in places:
#     print(f'Owner: {place.owner}')
#     print(f'added at: {place.created_at}')
#     print(f'type: {place.type()}\n')

print(type(places))