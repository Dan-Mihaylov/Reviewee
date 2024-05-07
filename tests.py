import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewee_app.settings")
django.setup()


# From here down
from django.utils import timezone
from django.db.models.functions import datetime
from django.shortcuts import reverse, resolve_url
from datetime import timedelta
from reviewee_app.booking.models import RestaurantBooking
from reviewee_app.booking.helpers import filter_place_bookings_for_date



bookings = RestaurantBooking.objects.all()
date_today = datetime.datetime.now().date()
print(f"Starting date: {date_today}")
for i in range(1, 8):
    print((date_today + timedelta(days=i)).strftime('%Y/%m/%d'))


