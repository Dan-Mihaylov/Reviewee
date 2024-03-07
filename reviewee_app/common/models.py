from django.db import models


class AuditModelMixin(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    edited_at = models.DateTimeField(
        auto_now=True,
    )
