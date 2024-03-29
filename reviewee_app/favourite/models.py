from django.db import models
from django.contrib.auth import get_user_model
from reviewee_app.common.models import AuditModelMixin
from ..place.models import Restaurant, Hotel

UserModel = get_user_model()


class BaseFavourite(AuditModelMixin, models.Model):

    class Meta:
        abstract = True
        ordering = ['-created_at']

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )


class FavouriteRestaurant(BaseFavourite):

    class Meta(BaseFavourite.Meta):
        unique_together = ['user', 'restaurant']

    restaurant = models.ForeignKey(
        Restaurant,
        related_name='favourite_to_users',
        on_delete=models.CASCADE,
        null=False,
        blank=True
    )

    def __str__(self):
        return f'{self.restaurant.name} Favourite to: {self.user.profile.get_name}'


class FavouriteHotel(BaseFavourite):

    class Meta(BaseFavourite.Meta):
        unique_together = ['user', 'hotel']

    hotel = models.ForeignKey(
        Hotel,
        related_name='favourite_to_users',
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    def __str__(self):
        return f'{self.hotel.name} Favourite to: {self.user.profile.get_name}'

