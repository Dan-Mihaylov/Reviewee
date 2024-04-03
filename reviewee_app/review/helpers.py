from django.contrib.auth import get_user_model
from django.db.models import QuerySet


UserModel = get_user_model()


# def find_user_liked_reviews_by_review_type(user: UserModel, review_type: str) -> QuerySet:
#
#     available_review_types = {
#         'HotelReview': user.hotelreview_set,
#         'RestaurantReview': user.restaurantreview_set,
#     }
#
#     if user.is_authenticated:
#         liked_reviews = user.available_review_types[review_type].all()
#         return liked_reviews
#
#     return QuerySet

