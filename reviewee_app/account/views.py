from django.shortcuts import render, HttpResponse

# Create your views here.
def register(request):
    return HttpResponse('Register Page')


def login(request):
    return HttpResponse('Login Page')


def logout(request):
    return HttpResponse('Logout Page')


def my_account_details(request):
    return HttpResponse('My account details page')


def account_details(request, pk: int):
    return HttpResponse('Account details page')


def account_edit(request):
    return HttpResponse('Account Edit page')


def account_delete(request):
    return HttpResponse('Account Delete page')

