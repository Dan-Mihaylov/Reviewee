import datetime
import time
from typing import Any
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_async_booking_mail_confirmation(
        subject: Any,
        message: Any,
        from_email: Any,
        recipient_list: Any,
        fail_silently: bool = False,
        auth_user: Any = None,
        auth_password: Any = None,
        connection: Any = None,
        html_message: Any = None) -> int:

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently,
        auth_user,
        auth_password,
        connection,
        html_message
    )
