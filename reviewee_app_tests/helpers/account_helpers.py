from typing import Dict

from reviewee_app.account.models import CustomUserProfile

from django.contrib.auth import get_user_model


UserModel = get_user_model()

USER_DATA = {
    'email': 'test@mail.com',
    'password': 'testpass321',
}


def create_owner_profile(user: UserModel) -> CustomUserProfile:
    profile = CustomUserProfile(
        user=user,
        owner=True,
    )
    profile.save()
    return profile


def create_user(credentials=USER_DATA) -> UserModel:
    user = UserModel.objects.create(**credentials)
    return user

