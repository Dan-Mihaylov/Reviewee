from rest_framework import serializers

from reviewee_app.notification.models import Notification


class NotificationForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationForReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['pk', 'read']

