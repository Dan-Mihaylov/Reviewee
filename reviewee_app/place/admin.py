from django.contrib import admin
from .models import Restaurant, Hotel


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'country', 'created_at', 'edited_at']
    list_filter = ['country', 'city', 'owner']
    search_fields = ['country', 'city']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'country', 'city', 'created_at', 'edited_at']
    list_filter = ['country','city' , 'owner']
    search_fields = ['country', 'city']

