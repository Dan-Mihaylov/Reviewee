from django.urls import path
from . import views

urlpatterns = [
    path('<str:place_slug>/<int:user_pk>/', views.favourite_functionality, name='favourite'),
    path('', views.FavouritePlacesListView.as_view(), name='user favourite places'),
]

