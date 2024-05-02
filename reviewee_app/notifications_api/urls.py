from django.urls import path
from . import views


urlpatterns = [
    path('notifications/', views.NotificationApiListView.as_view(), name='api-notifications'),
    path('toggle-read/<int:pk>/', views.NotificationToggleRead.as_view(), name='api-toggle-read'),
    path('notification/destroy/<int:pk>', views.NotificationDestroyView.as_view(), name='api-delete-notification'),
    path('unread-notifications-count/', views.NotificationUnreadCountView.as_view(), name='api-count-unread-notifications')
]

