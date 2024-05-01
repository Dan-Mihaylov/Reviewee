from django.urls import path
from . import views


urlpatterns = [
    path('notifications/', views.NotificationApiListView.as_view(), name='api-notifications'),
    path('mark-read/<int:pk>/', views.NotificationToggleRead.as_view(), name='api-toggle-read'),
]

