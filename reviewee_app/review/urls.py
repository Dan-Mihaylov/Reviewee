from django.urls import path
from . import views

urlpatterns = [
    path('write/<slug:place_slug>/', views.ReviewWriteView.as_view(), name='review write'),
    path('<int:pk>/edit/', views.place_review_edit, name='review edit'),
    path('<int:pk>/delete/', views.place_review_delete, name='review delete'),
]