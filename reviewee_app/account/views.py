from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.forms import modelform_factory
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login, views as auth_views, \
    get_user_model
from django.urls import reverse
from django.views import generic as views

from reviewee_app.account.forms import CustomUserCreationForm
from reviewee_app.favourite.helpers import get_users_favourite_places
from reviewee_app.place.helpers import get_users_places
from reviewee_app.account.models import CustomUserProfile, CustomUserBusinessProfile


UserModel = get_user_model()


class RegisterView(views.CreateView):
    template_name = 'account/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        auth_login(self.request, self.object)
        return reverse('profile edit')


class LoginView(auth_views.LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass


class ProfileDetailsView(views.DetailView):
    template_name = 'account/profile_details.html'

    def get_queryset(self):
        return UserModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_places'] = get_users_places(self.object.pk)
        context['users_favourites'] = get_users_favourite_places(self.request.user)
        return context


class EditProfileView(views.UpdateView):

    template_name = 'account/edit_profile.html'

    def get_object(self, queryset=None):
        try:
            return CustomUserProfile.objects.get(pk=self.request.user.pk)

        except ObjectDoesNotExist:
            return redirect('home')

        except MultipleObjectsReturned:
            return redirect('home')

    def get_form_class(self):
        return modelform_factory(CustomUserProfile, exclude=['owner'])

    def get_success_url(self):
        if self.object.is_owner():
            return reverse('business profile edit')
        return reverse('profile details', kwargs={'pk': self.request.user.pk})


class EditBusinessProfileView(views.UpdateView):

    template_name = 'account/edit_business_profile.html'

    def get_object(self, queryset=None):
        try:
            return CustomUserBusinessProfile.objects.get(pk=self.request.user.pk)

        except ObjectDoesNotExist:
            return redirect('home')

        except MultipleObjectsReturned:
            return redirect('home')

    def get_form_class(self):
        return modelform_factory(CustomUserBusinessProfile, fields='__all__')

    def get_success_url(self):
        return reverse('profile details', kwargs={'pk': self.object.user.pk})


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'account/password-change.html'

    def get_success_url(self):
        return reverse('profile details', kwargs={'pk': self.request.user.pk})


class ProfileDeleteView(views.DeleteView):
    template_name = 'account/profile_delete.html'

    def get_object(self, queryset=None):
        return UserModel.objects.get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse('home')


