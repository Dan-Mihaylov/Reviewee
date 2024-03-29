from django.contrib import admin
from .models import FavouriteHotel, FavouriteRestaurant


@admin.register(FavouriteHotel)
class FavouriteHotelAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'created_at']


@admin.register(FavouriteRestaurant)
class FavouriteRestaurantAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'created_at']
