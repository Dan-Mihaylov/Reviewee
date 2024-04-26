from django.db import models
from django.contrib.auth import get_user_model

from reviewee_app.common.models import AuditModelMixin


UserModel = get_user_model()


class Notification(AuditModelMixin, models.Model):
    MAX_LENGTH_TEXT_FIELD = 500
    MAX_LENGTH_TYPE_FIELD = 10
    NOTIFICATION_TYPE_CHOICES = (
        ('Account', 'Account'),
        ('Likes', 'Likes'),
        ('Bookings', 'Bookings'),
        ('Reviews', 'Reviews')
    )

    user = models.ForeignKey(
        UserModel,
        related_name='notifications',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    text = models.TextField(
        max_length=MAX_LENGTH_TEXT_FIELD,
        null=False,
        blank=False,
    )

    read = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    link = models.URLField(
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=MAX_LENGTH_TYPE_FIELD,
        choices=NOTIFICATION_TYPE_CHOICES,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'Notification for {self.user}'
