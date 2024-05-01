from rest_framework.response import Response
from rest_framework import generics as api_views, status

from reviewee_app.notification.models import Notification
from .serializers import NotificationForListSerializer, NotificationForReadSerializer


class NotificationApiListView(api_views.ListAPIView):

    serializer_class = NotificationForListSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        print('In it')
        return super().get(request, *args, **kwargs)


class NotificationToggleRead(api_views.RetrieveUpdateAPIView):

    serializer_class = NotificationForReadSerializer

    def get_queryset(self):
        return Notification.objects.all()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read = not instance.read
        instance.save()
        serializer = self.get_serializer(instance)
        print('okay')
        return Response(serializer.data)
