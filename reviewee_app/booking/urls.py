from django.urls import path, include
from . import views

urlpatterns = [
    path('place/<slug>/', views.book_place, name='book place'),
    path('all/', views.booking_all, name='booking all'),
    path('<pk>/', include(
        [
            path('details/', views.booking_details, name='booking details'),
            path('cancel/', views.booking_cancel, name='booking cancel'),
        ]
    )),

]