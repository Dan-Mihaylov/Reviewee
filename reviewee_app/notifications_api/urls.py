from django.urls import path
from . import views


urlpatterns = [
    path('notifications/', views.NotificationApiListView.as_view(), name='api-notifications'),
    path('mark-read/', views.NotificationMarkRead.as_view(), name='api-mark-read'),
]

