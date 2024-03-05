from django.db import models
from django.contrib.auth.models import AbstractUser
from . import managers


class CustomUser(AbstractUser):
    MAX_GENDER_LENGTH = 12

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    owner = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    gender = models.CharField(
        max_length=MAX_GENDER_LENGTH,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.CustomUserManager()

    # TODO Create functions to display name, username, email, and if is owner

    def __str__(self):
        return f'{self.email}'



