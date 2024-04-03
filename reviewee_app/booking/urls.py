from django.urls import path, include
from . import views

urlpatterns = [
    path('restaurant/<place_slug>/', views.BookingBookRestaurantView.as_view(), name='book restaurant'),
    path('hotel/<place_slug>/', views.BookingBookHotel.as_view(), name='book hotel'),
    path('successful/', views.BookingSuccessfulView.as_view(), name='booking successful'),
    path('find/', views.BookingFindView.as_view(), name='find booking'),
    path('verify-ownership/<slug:slug>/', views.BookingVeryfiOwnershipView.as_view(), name='verify ownership'),
    path('manage/<slug>', views.BookingManageView.as_view(), name='manage booking'),
    path('', views.booking_all,)

]