from django.contrib import admin
from .models import RestaurantReview, HotelReview


@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):

    list_display = ['pk', 'user', 'restaurant', 'created_at', 'edited_at']


@admin.register(HotelReview)
class HotelReviewAdmin(admin.ModelAdmin):
        list_display = ['pk', 'user', 'hotel', 'created_at', 'edited_at']

