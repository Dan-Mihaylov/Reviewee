from django.forms import modelform_factory
from django.shortcuts import render, HttpResponse, redirect

from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate, views as auth_views, \
    get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from django.views import generic as views

from reviewee_app.account.forms import CustomLoginForm, CustomUserCreationForm, CustomUserChangeForm
from reviewee_app.account.models import CustomUserProfile

UserModel = get_user_model()


# You register and chose if you are or not an owner, then it takes you to profile edit page, straight away, with
# success url, and if you are an owner, you get both forms displayed. The CustomUserProfile & CustomUserBusinessProfile
def register(request):
    return HttpResponse('Register Page')


class RegisterView(views.CreateView):
    template_name = 'account/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        auth_login(self.request, self.object)
        return reverse('home')


# TODO migrate to Class Based Views
def login(request):

    form = CustomLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid:

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')

    context = {
        'form': form,
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


def account_delete(request):
    return HttpResponse('Account Delete page')

