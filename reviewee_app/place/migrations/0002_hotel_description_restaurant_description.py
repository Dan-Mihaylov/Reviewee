# Generated by Django 5.0.2 on 2024-03-19 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='description',
            field=models.TextField(default='this is default foor now'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='description',
            field=models.TextField(default='this is default foor now'),
        ),
    ]
