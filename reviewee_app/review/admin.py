from django.contrib import admin
from .models import RestaurantReview, HotelReview, HotelReviewLike, RestaurantReviewLike


@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):

    list_display = ['pk', 'user', 'restaurant', 'created_at', 'edited_at']


@admin.register(HotelReview)
class HotelReviewAdmin(admin.ModelAdmin):

        list_display = ['pk', 'user', 'hotel', 'created_at', 'edited_at']


@admin.register(RestaurantReviewLike)
class RestaurantReviewLikeAdmin(admin.ModelAdmin):

    list_display = ['pk', 'user', 'restaurant_review', 'created_at']


@admin.register(HotelReviewLike)
class HotelReviewLikeAdmin(admin.ModelAdmin):

    list_display = ['pk', 'user', 'hotel_review', 'created_at']
