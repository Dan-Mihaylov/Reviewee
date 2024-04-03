from django.urls import path
from . import views

urlpatterns = [
    path('write/<slug:place_slug>/', views.ReviewWriteView.as_view(), name='review write'),
    path('edit/<slug:place_slug>/<int:id>/', views.ReviewEditView.as_view(), name='review edit'),
    path('delete/<place_slug>/<int:id>/', views.ReviewDeleteView.as_view(), name='review delete'),
    path('like/<review_type>/<review_pk>/<int:pk>', views.ReviewLike.as_view(), name='review like'),
]
