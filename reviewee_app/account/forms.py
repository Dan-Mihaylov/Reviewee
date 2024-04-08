from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from django import forms
from .models import CustomUserProfile, CustomUserBusinessProfile

UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    business_owner = forms.BooleanField(
        required=False,
    )

    class Meta:
        model = UserModel
        fields = ['email']

    def _is_business_owner(self):
        return self.cleaned_data['business_owner']

    def save(self, commit=True):
        user = super().save(commit=commit)

        is_owner = self._is_business_owner()

        custom_user_profile = CustomUserProfile(
            user=user,
            owner=is_owner
        )

        if commit:
            custom_user_profile.save()

        if is_owner:
            custom_user_business_profile = CustomUserBusinessProfile(user=user)
            custom_user_business_profile.save()

        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserModel
        fields = '__all__'
