# Generated by Django 5.0.2 on 2024-03-06 23:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_customuserprofile_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuserbusinessprofile',
            name='user',
            field=models.OneToOneField(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='business_profile', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuserprofile',
            name='user',
            field=models.OneToOneField(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
