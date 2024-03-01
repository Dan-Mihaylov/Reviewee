from django.db import models


class CreatedAtModelMixin(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class EditedAtModelMixin(models.Model):

    class Meta:
        abstract = True

    edited_at = models.DateTimeField(
        auto_now=True,
    )
