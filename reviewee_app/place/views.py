from django.shortcuts import render, HttpResponse


def place_add(request):
    return render(request, 'place/place-add.html')


def place_details(request, slug):
    return HttpResponse('Place Details Page')


def place_bookings(request, slug):
    return HttpResponse('Place Bookings Page')


def place_edit(request, slug):
    return HttpResponse('Place Edit Page')


def place_delete(request, slug):
    return HttpResponse('Place Delete Page')


def place_review_write(request, slug):
    return HttpResponse('Place Review Write Page')


def place_review_edit(request, slug, pk):
    return HttpResponse('Place Review Edit Page')


def place_review_delete(request, slug, pk):
    return HttpResponse('Place Review Delete Page')
