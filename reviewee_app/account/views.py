from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect

from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate, views as auth_views, \
    get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from django.views import generic as views

from reviewee_app.account.forms import CustomLoginForm, CustomUserCreationForm, CustomUserChangeForm
from reviewee_app.account.models import CustomUserProfile, CustomUserBusinessProfile

UserModel = get_user_model()


# You register and chose if you are or not an owner, then it takes you to profile edit page, straight away, with
# success url, and if you are an owner, you get both forms displayed. The CustomUserProfile & CustomUserBusinessProfile
class RegisterView(views.CreateView):
    template_name = 'account/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        auth_login(self.request, self.object)
        return reverse('home')


# TODO migrate to Class Based Views
def login(request):

    errors = ''

    form = CustomLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid:

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            errors = 'Something went wrong. Make sure email and password match for the account.'

    context = {
        'form': form,
        'errors': errors,
    }

    return render(request, 'account/login.html', context)


def logout(request):

    auth_logout(request)
    return redirect('home')


def my_account_details(request):
    return HttpResponse('My account details page')


def account_details(request, pk: int):
    return HttpResponse('Account details page')


def account_edit(request):
    return HttpResponse('Account Edit page')


class EditProfileView(views.UpdateView):

    template_name = 'account/edit_profile.html'

    # After the exception, need to create a message for it
    def get_object(self, queryset=None):
        try:
            return CustomUserProfile.objects.get(pk=self.request.user.pk)
        except ObjectDoesNotExist or MultipleObjectsReturned:
            return redirect('home')

    def get_form_class(self):
        return modelform_factory(CustomUserProfile, exclude=['owner'])

    # TODO change redirect to account info
    def get_success_url(self):
        if self.object.is_owner():
            return reverse('business profile edit')
        return reverse('home')


class EditBusinessProfileView(views.UpdateView):

    template_name = 'account/edit_business_profile.html'

    # After the exception, need to create a message for it
    def get_object(self, queryset=None):
        try:
            return CustomUserBusinessProfile.objects.get(pk=self.request.user.pk)
        except ObjectDoesNotExist or MultipleObjectsReturned:
            return redirect('home')

    def get_form_class(self):
        return modelform_factory(CustomUserBusinessProfile, fields='__all__')

    # TODO change redirect to account info
    def get_success_url(self):
        return reverse('home')


def account_delete(request):
    return HttpResponse('Account Delete page')

