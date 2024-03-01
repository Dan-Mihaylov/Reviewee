from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.db import models

from . import validators
from reviewee_app.common.mixins.model_mixins import CreatedAtModelMixin, EditedAtModelMixin


UserModel = get_user_model()


class BasePlaceModel(CreatedAtModelMixin, EditedAtModelMixin, models.Model):
    
    MIN_LENGTH_PLACE_NAME = 3
    MAX_LENGTH_PLACE_NAME = 50
    MAX_LENGTH_ADDRESS = 120
    MAX_LENGTH_POSTCODE = 10
    DEFAULT_MAX_CHAR_LENGTH = 32
    DEFAULT_MIN_CHAR_LENGTH = 2
    DEFAULT_MIN_LENGTH_VALIDATION_ERROR_MESSAGE = f'You have to use minimum of {DEFAULT_MIN_CHAR_LENGTH} characters.'
    MIN_LENGTH_PLACE_VALIDATION_ERROR_MESSAGE = f'The place name must be at least {MIN_LENGTH_PLACE_NAME} characters long.'
   
    class Meta:
        abstract=True

    photo = models.ImageField(
        upload_to='images/place/photos'
    )

    name = models.CharField(
        max_length=MAX_LENGTH_PLACE_NAME,
        validators=[
            validators.alphanumeric_and_spaces_values_validator,
            MinLengthValidator(MIN_LENGTH_PLACE_NAME, MIN_LENGTH_PLACE_VALIDATION_ERROR_MESSAGE),
        ],
        null=False,
        blank=False,
    )
    
    owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )
    
    country = models.CharField(
        max_length=DEFAULT_MAX_CHAR_LENGTH,
        null=False,
        blank=False,
    )
    
    city = models.CharField(
        max_length=DEFAULT_MAX_CHAR_LENGTH,
        validators=[
            MinLengthValidator(DEFAULT_MIN_CHAR_LENGTH, DEFAULT_MIN_LENGTH_VALIDATION_ERROR_MESSAGE),
            validators.only_letters_and_spaces_values_validator,
        ],
        null=False,
        blank=False,
    )

    address = models.CharField(
        max_length=MAX_LENGTH_ADDRESS,
        validators=[
            MinLengthValidator(DEFAULT_MIN_CHAR_LENGTH, DEFAULT_MIN_LENGTH_VALIDATION_ERROR_MESSAGE),
            validators.alphanumeric_and_spaces_values_validator,
        ],
        null=False,
        blank=False,
    )
    
    post_code = models.CharField(
        max_length=MAX_LENGTH_POSTCODE,
        validators=[
            MinLengthValidator(DEFAULT_MIN_CHAR_LENGTH, DEFAULT_MIN_LENGTH_VALIDATION_ERROR_MESSAGE),
            validators.alphanumeric_and_spaces_values_validator,
        ],
        null=True,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
        editable=False,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # TODO maybe it will be saving, restaurants and hotels with same slug, if id == same and name == same???
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.pk}')
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.country}'


class Restaurant(BasePlaceModel):
    class Meta:
        default_related_name = 'restaurants'

    MIN_SEATS_COUNT = 10
    MIN_SEAT_COUNT_VALIDATION_ERROR_MESSAGE = f'Seats must be at least {MIN_SEATS_COUNT}.'

    opening_time = models.TimeField(
        null=False,
        blank=False,
    )

    closing_time = models.TimeField(
        null=False,
        blank=False,
    )

    available_seats = models.PositiveIntegerField(
        validators=[
            MinValueValidator(MIN_SEATS_COUNT, MIN_SEAT_COUNT_VALIDATION_ERROR_MESSAGE),
        ],
        null=False,
        blank=False,
    )


class Hotel(BasePlaceModel):

    class Meta:
        default_related_name = 'hotels'

    MIN_ROOMS_COUNT = 3
    MIN_ROOM_COUNT_VALIDATION_ERROR_MESSAGE = f'Rooms must be {MIN_ROOMS_COUNT} or over.'

    check_in_time = models.TimeField(
        null=False,
        blank=False,
    )

    check_out_time = models.TimeField(
        null=False,
        blank=False,
    )

    available_rooms = models.PositiveIntegerField(
        validators=[
          MinValueValidator(MIN_ROOMS_COUNT, MIN_ROOM_COUNT_VALIDATION_ERROR_MESSAGE)
        ],
    )


