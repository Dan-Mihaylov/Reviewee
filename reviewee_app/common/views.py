from django.shortcuts import render, HttpResponse


def home_page(request):
    return render(request, 'common/index.html')