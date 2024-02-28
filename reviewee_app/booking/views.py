from django.shortcuts import render, HttpResponse


def book_place(request, slug):  # place slug
    return HttpResponse('Book Place Page')


def booking_all(request):
    return HttpResponse('All My Bookings Page')


def booking_details(request, pk):
    return HttpResponse('Booking Details Page')


def booking_cancel(request, pk):
    return HttpResponse('Booking Cancel Page')

