from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', include(
        [
            path('', views.PlaceAddView.as_view(), name='place add'),
            path('restaurant/', views.RestaurantAddView.as_view(), name='restaurant add'),
            path('hotel/', views.HotelAddView.as_view(), name='hotel add'),
        ]
    )),
    path('<slug>/', include(
        [
            path('', views.PlaceDetailsView.as_view(), name='place details'),
            path('edit/', views.PlaceEditView.as_view(), name='place edit'),
            path('delete/', views.PlaceDeleteView.as_view(), name='place delete'),
            path('bookings/', views.place_bookings, name='place bookings'),
        ]
    )),
]
