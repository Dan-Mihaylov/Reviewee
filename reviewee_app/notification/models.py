from django.db import models
from django.contrib.auth import get_user_model

from reviewee_app.common.models import AuditModelMixin


UserModel = get_user_model()


class Notification(AuditModelMixin, models.Model):
    MAX_LENGTH_TEXT_FIELD = 500

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

    def __str__(self):
        return f'Notification for {self.user}'
