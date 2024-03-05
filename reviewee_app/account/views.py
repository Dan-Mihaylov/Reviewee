from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def register(request):
    return HttpResponse('Register Page')


def login(request):

    form = AuthenticationForm(request.POST or None)
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

