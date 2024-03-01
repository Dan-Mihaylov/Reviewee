import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewee_app.settings")
django.setup()


# From here down
from django.contrib.auth import get_user_model


UserModel = get_user_model()
user = UserModel.objects.get(pk=1)
restaurants = user.restaurants.all()
print(restaurants)

hotels = user.hotels.all()
print(list(hotels))