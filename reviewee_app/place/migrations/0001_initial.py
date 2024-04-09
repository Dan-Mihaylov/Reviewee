# Generated by Django 5.0.4 on 2024-04-08 23:34

import django.core.validators
import django.db.models.deletion
import reviewee_app.common.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(upload_to='images/place/photos')),
                ('name', models.CharField(max_length=50, validators=[reviewee_app.common.validators.alphanumeric_and_spaces_values_validator, django.core.validators.MinLengthValidator(3, 'The place name must be at least 3 characters long.')])),
                ('description', models.TextField()),
                ('country', models.CharField(max_length=32)),
                ('city', models.CharField(max_length=32, validators=[django.core.validators.MinLengthValidator(2, 'You have to use minimum of 2 characters.'), reviewee_app.common.validators.only_letters_and_spaces_values_validator])),
                ('address', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(2, 'You have to use minimum of 2 characters.'), reviewee_app.common.validators.alphanumeric_and_spaces_values_validator])),
                ('post_code', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(2, 'You have to use minimum of 2 characters.'), reviewee_app.common.validators.alphanumeric_and_spaces_values_validator])),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('check_in_time', models.TimeField()),
                ('check_out_time', models.TimeField()),
                ('available_rooms', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(3, 'Rooms must be 3 or over.')])),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_related_name': 'hotels',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(upload_to='images/place/photos')),
                ('name', models.CharField(max_length=50, validators=[reviewee_app.common.validators.alphanumeric_and_spaces_values_validator, django.core.validators.MinLengthValidator(3, 'The place name must be at least 3 characters long.')])),
                ('description', models.TextField()),
                ('country', models.CharField(max_length=32)),
                ('city', models.CharField(max_length=32, validators=[django.core.validators.MinLengthValidator(2, 'You have to use minimum of 2 characters.'), reviewee_app.common.validators.only_letters_and_spaces_values_validator])),
                ('address', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(2, 'You have to use minimum of 2 characters.'), reviewee_app.common.validators.alphanumeric_and_spaces_values_validator])),
                ('post_code', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(2, 'You have to use minimum of 2 characters.'), reviewee_app.common.validators.alphanumeric_and_spaces_values_validator])),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('available_seats', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(10, 'Seats must be at least 10.')])),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_related_name': 'restaurants',
            },
        ),
    ]
