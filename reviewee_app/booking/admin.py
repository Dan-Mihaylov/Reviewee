from django.contrib import admin
from .models import RestaurantBooking, HotelBooking


@admin.register(RestaurantBooking)
class RestaurantBookingAdmin(admin.ModelAdmin):
    list_display = ['slug', 'restaurant', 'first_name', 'date', 'booking_time', 'confirmation_code']


@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ['slug', 'hotel', 'first_name', 'date', 'nights', 'rooms', 'confirmation_code']
