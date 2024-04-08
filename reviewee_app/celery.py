import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reviewee_app.settings')

app = Celery('reviewee_app')

# Get the configuration of celery from the project settings.py it will take everything with the CELERY in it.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
