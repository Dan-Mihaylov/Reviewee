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
            path('', views.place_details, name='place details'),
            path('edit/', views.place_edit, name='place edit'),
            path('delete/', views.place_delete, name='place delete'),
            path('bookings/', views.place_bookings, name='place bookings'),
            path('review/', include(
                [
                    path('write/', views.place_review_write, name='place review write'),
                    path('<int:pk>/edit/', views.place_review_edit, name='place review edit'),
                    path('<int:pk>/delete/', views.place_review_delete, name='place review delete'),
                ]
            ))
        ]
    )),
]
