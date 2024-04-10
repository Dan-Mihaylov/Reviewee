from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from reviewee_app.place.models import Hotel, Restaurant
from reviewee_app.account.models import AuditModelMixin
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Review(AuditModelMixin, models.Model):

    class Meta:
        abstract = True
        ordering = ['-edited_at']

    MAX_LENGTH_CONTENT = 2000

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=False,
        blank=True
    )

    comment = models.TextField(
        max_length=MAX_LENGTH_CONTENT,
        null=False,
        blank=False,
    )

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    review_photo = models.ImageField(
        upload_to= 'images/review/photos',
        null=True,
        blank=True,
    )

    def type(self):
        return self.__class__.__name__


class HotelReview(Review):

    class Meta(Review.Meta):
        unique_together = ['hotel', 'user']

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=False,
        blank=True,
    )


class RestaurantReview(Review):

    class Meta(Review.Meta):
        unique_together = ['restaurant', 'user']

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=False,
        blank=True,
    )


class BaseReviewLike(AuditModelMixin, models.Model):

    class Meta:
        abstract = True
        ordering = ['-created_at']

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    def count(self):
        return self.objects.count()


class RestaurantReviewLike(BaseReviewLike):

    class Meta(BaseReviewLike.Meta):
        unique_together = ['user', 'restaurant_review']

    restaurant_review = models.ForeignKey(
        RestaurantReview,
        related_name='likes',
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    def __str__(self):
        return f'{self.user} likes {self.restaurant_review}'


class HotelReviewLike(BaseReviewLike):

    class Meta(BaseReviewLike.Meta):
        unique_together = ['user', 'hotel_review']

    hotel_review = models.ForeignKey(
        HotelReview,
        related_name='likes',
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    def __str__(self):
        return f'{self.user} likes {self.hotel_review}'
