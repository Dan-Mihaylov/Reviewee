from django.contrib import admin
from .models import Restaurant, Hotel


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    # TODO add all the filtering and searching functionality in the admin page
    list_display = ['name', 'owner', 'country', 'created_at', 'edited_at']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'country', 'city', 'created_at', 'edited_at']

