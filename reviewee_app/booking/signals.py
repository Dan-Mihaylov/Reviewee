from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.template.loader import render_to_string

from .tasks import send_async_booking_mail_confirmation
from .models import HotelBooking, RestaurantBooking
from .. import settings


@receiver(post_save)
def send_mail_on_booking_creation(sender, instance, created, **kwargs):

    if created and sender in (HotelBooking, RestaurantBooking):

        subject = (
            f'Booking confirmation for '
            f'{instance.restaurant.name if hasattr(instance, "restaurant") else instance.hotel.name}'
        )

        message = (
            f'Thank you for booking with Reviewee.\n\n'
            f'Dear {instance.first_name} {instance.last_name} this is to confirm your reservation at the,'
            f'{instance.restaurant.name if hasattr(instance, "restaurant") else instance.hotel.name}'
            f'{"Restaurant" if hasattr(instance, "restaurant") else "Hotel"}'
            f'your confirmation code is "{instance.confirmation_code}".\n\n'
            f'For more information about your reservation, or if you would like to do amend or cancel your'
            f' reservation please visit: '
            f'http://127.0.0.1:8000/booking/find\n\n'
            f'Sincere, Reviewee team.'
        )

        html_message = render_to_string(
            'partials/booking-confirmation-email.html',
            context={
                'instance': instance,
                'restaurant': hasattr(instance, 'restaurant'),
            }
        )

        # from_email = ''
        recipient_list = [instance.email,]

        send_async_booking_mail_confirmation.delay(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
            html_message=html_message,
        )
