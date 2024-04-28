from rest_framework.response import Response
from rest_framework import generics as api_views, status

from reviewee_app.notification.models import Notification
from .serializers import NotificationForListSerializer, NotificationForReadSerializer


class NotificationApiListView(api_views.ListAPIView):

    serializer_class = NotificationForListSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    # def get(self, request, *args, **kwargs):
    #


class NotificationMarkRead(api_views.UpdateAPIView):
    pass
