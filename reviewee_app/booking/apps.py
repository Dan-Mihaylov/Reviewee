from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviewee_app.booking'

    def ready(self):
        import reviewee_app.booking.signals
