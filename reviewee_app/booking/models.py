from datetime import datetime, time

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

from reviewee_app.booking.model_helpers import generate_random_confirmation_code
from reviewee_app.common.models import AuditModelMixin
from reviewee_app.common.validators import only_letters_and_spaces_values_validator
from reviewee_app.place.models import Restaurant, Hotel

UserModel = get_user_model()


class BaseBooking(AuditModelMixin, models.Model):
    MAX_LENGTH_NAMES = 32
    MAX_LENGTH_EMAIL = 120
    MAX_LENGTH_RANDOM_CONFIRMATION_CODE = 6

    class Meta:
        abstract = True
        ordering = ['-created_at']

    date = models.DateField(
        validators=[MinValueValidator(limit_value=timezone.now().date(),)]
    )

    first_name = models.CharField(
        max_length=MAX_LENGTH_NAMES,
        validators=[only_letters_and_spaces_values_validator, ],
        null=False,
        blank=False,
    )

    last_name = models.CharField(
        max_length=MAX_LENGTH_NAMES,
        validators=[only_letters_and_spaces_values_validator, ],
        null=False,
        blank=False,
    )

    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        null=False,
        blank=False,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
        editable=False,
    )

    confirmation_code = models.CharField(
        max_length=MAX_LENGTH_RANDOM_CONFIRMATION_CODE,
        default=generate_random_confirmation_code,
        null=False,
        blank=True,
        editable=False,
    )

    canceled = models.BooleanField(
        default=False,
        null=False,
        blank=True,
    )

    active = models.BooleanField(
        default=True,
        null=False,
        blank=True,
    )

    def type(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.pk}-{self.__class__.__name__}')

        return super().save(*args, **kwargs)


class RestaurantBooking(BaseBooking):

    MIN_PEOPLE_FOR_BOOKING = 1
    MAX_PEOPLE_FOR_BOOKING = 6
    MIN_PEOPLE_VALIDATION_MESSAGE = f'Minimum {MIN_PEOPLE_FOR_BOOKING} person required for booking.'
    MAX_PEOPLE_VALIDATION_MESSAGE = f'Maximum of {MAX_PEOPLE_FOR_BOOKING} people allowed per booking.'

    @staticmethod
    def time_slot_choices():
        choices = []

        for hour in range(0, 24):
            for minute in range(0, 60, 30):
                slot = time(hour, minute)
                text = slot.strftime('%H:%M')
                choices.append((slot, text))

        return choices

    restaurant = models.ForeignKey(
        Restaurant,
        related_name='bookings',
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    booking_time = models.TimeField(
        choices=time_slot_choices(),
        null=False,
        blank=False,
    )

    people = models.PositiveIntegerField(
        validators=[
            MinValueValidator(MIN_PEOPLE_FOR_BOOKING, MIN_PEOPLE_VALIDATION_MESSAGE),
            MaxValueValidator(MAX_PEOPLE_FOR_BOOKING, MAX_PEOPLE_VALIDATION_MESSAGE),
        ]
    )

    def clean(self):

        booking_time_restaurant_working_hours_validation_error_message = (
            f'Booking time must be between {self.restaurant.opening_time} '
            f'and {self.restaurant.closing_time} for restaurant {self.restaurant.name}'
        )
        booking_time_in_the_past_for_today_validation_error_message = (
            f'Booking time must be in the future.'
        )

        super().clean()
        if self.booking_time and hasattr(self, 'restaurant'):

            if self.booking_time < self.restaurant.opening_time or self.booking_time > self.restaurant.closing_time:
                raise ValidationError(booking_time_restaurant_working_hours_validation_error_message)

            if self.date == datetime.now().date() and self.booking_time < datetime.now().time():
                raise ValidationError(booking_time_in_the_past_for_today_validation_error_message)

    def __str__(self):
        return f'Reservation at {self.restaurant.name} for {self.first_name} {self.last_name}'


class HotelBooking(BaseBooking):

    MAX_ROOMS_PER_BOOKING = 3
    MIN_ROOMS_PER_BOOKING = 1
    MIN_NIGHTS_PER_BOOKING = 1
    MAX_NIGHTS_PER_BOOKING = 14

    hotel = models.ForeignKey(
        Hotel,
        related_name='bookings',
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    rooms = models.PositiveIntegerField(
        validators=[
            MinValueValidator(MIN_ROOMS_PER_BOOKING),
            MaxValueValidator(MAX_ROOMS_PER_BOOKING)
        ],
        null=False,
        blank=False,
    )

    nights = models.PositiveIntegerField(
        validators=[
            MinValueValidator(MIN_NIGHTS_PER_BOOKING),
            MaxValueValidator(MAX_NIGHTS_PER_BOOKING),
        ],
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'Reservation at {self.hotel.name} for {self.first_name} {self.last_name}'

