from django.urls import path, include
from . import views

urlpatterns = [
    path('place/<place_slug>/', views.BookingBookRestaurantView.as_view(), name='book restaurant'),
    path('successful', views.BookingSuccessfulView.as_view(), name='booking successful'),
    path('', views.booking_all,)

]