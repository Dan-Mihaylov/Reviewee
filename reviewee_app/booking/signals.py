from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import HotelBooking, RestaurantBooking


@receiver(post_save)
def send_mail_on_booking_creation(sender, instance, created, **kwargs):

    if created and sender in (HotelBooking, RestaurantBooking):
        # TODO send mail logic
        print('Booking created for')
        print(instance.first_name)
        print(instance.last_name)
        print(instance.email)
        print(instance.date)
        print(instance.confirmation_code)
        print(instance)

        subject = f'Booking confirmation'
        message = (f'Hello {instance.first_name} {instance.last_name} this is to confirm your booking'
                   f'your confirmation code is "{instance.confirmation_code}" to do any changes'
                   f'for changes to your booking go to the website.')
        from_email = 'reviewee.app@outlook.com'
        recipient_list = [instance.email,]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

