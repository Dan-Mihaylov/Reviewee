from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import models as auth_models, get_user_model

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db import models

from . import managers, helpers
from reviewee_app.common.models import AuditModelMixin
from reviewee_app.common import validators


class CustomUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        }
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.CustomUserManager()

    def __str__(self):
        return self.email


class GenderChoices(models.TextChoices):
    male = 'Male'
    female = 'Female'
    other = 'Other'


class CustomUserProfile(AuditModelMixin, models.Model):

    MAX_LENGTH_FIRST_NAME = 120
    MAX_LENGTH_LAST_NAME = 120
    MAX_LENGTH_USERNAME = 32
    MAX_LENGTH_GENDER = 10

    user = models.OneToOneField(
        CustomUser,
        related_name='profile',
        on_delete=models.CASCADE,
        primary_key=True,
        editable=False,
        null=False,
        blank=True,
    )

    owner = models.BooleanField(
        editable=True,
        default=False,
        null=True,
        blank=True,
    )

    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=[
            validators.alphanumeric_and_dashes_validator,
        ],
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_NAME,
        validators=[
            validators.only_letters_and_spaces_values_validator,
        ],
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=MAX_LENGTH_LAST_NAME,
        validators=[
            validators.only_letters_and_spaces_values_validator,
        ],
        null=True,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to=helpers.user_profile_photo_upload_path,
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=MAX_LENGTH_GENDER,
        choices=GenderChoices.choices,
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    def is_owner(self):
        return self.owner

    def __str__(self):
        return f'{self.pk}, {self.username}'

    def save(self, *args, **kwargs):

        # This is so the owner can be set only once, at creation of the profile
        try:
            # If it is the first time you create the instance it will raise attribute error
            instance = CustomUserProfile.objects.filter(user=self.user).first()

            if instance.owner or not instance.owner:
                self.owner = instance.owner
            return super().save(*args, **kwargs)

        except AttributeError:
            return super().save(*args, **kwargs)


class CustomUserBusinessProfile(AuditModelMixin ,models.Model):

    MAX_LENGTH_BUSINESS_NAME = 120
    MAX_LENGTH_COUNTRY = 50
    MAX_LENGTH_CITY = 50
    MAX_LENGTH_ADDRESS = 120
    MAX_LENGTH_POSTCODE = 10

    user = models.OneToOneField(
        CustomUser,
        related_name='business_profile',
        on_delete=models.CASCADE,
        primary_key=True,
        editable=False,
        null=False,
        blank=True,
    )

    business_name = models.CharField(
        max_length=MAX_LENGTH_BUSINESS_NAME,
        validators=[
            validators.only_letters_and_spaces_values_validator,
        ],
        null=True,
        blank=True,
    )

    country = models.CharField(
        max_length=MAX_LENGTH_COUNTRY,
        validators=[
            validators.check_country_name_validator,
        ],
        null=False,
        blank=False,
    )

    city = models.CharField(
        max_length=MAX_LENGTH_CITY,
        validators=[
            validators.only_letters_and_spaces_values_validator,
        ],
        null=False,
        blank=False,
    )

    address_line = models.CharField(
        max_length=MAX_LENGTH_ADDRESS,
        null=False,
        blank=False,
    )

    postcode = models.CharField(
        max_length=MAX_LENGTH_POSTCODE,
        null=False,
        blank=False,
    )

    # Only owners can create a business profile
    def save(self, *args, **kwargs):
        if self.user.profile.is_owner():
            return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.email}'
