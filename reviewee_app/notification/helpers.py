from .models import Notification
from django.contrib.auth import get_user_model


UserModel = get_user_model()


def create_notification_on_register(user: UserModel):

    text = f'You have successfully registered to Reviewee, explore, review and manage your places'
