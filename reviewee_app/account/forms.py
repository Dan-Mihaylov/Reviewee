from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

from django import forms
from .models import CustomUser, CustomUserProfile, CustomUserBusinessProfile

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
            owner = is_owner
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


# TODO maybe use a form from Bootstrap in the template
class CustomLoginForm(AuthenticationForm):

    # The username field is actually the 'email' field, since we used USERNAME_FIELD = 'email'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Enter your password',
            }
        )