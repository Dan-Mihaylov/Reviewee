from django.shortcuts import render, HttpResponse


# TODO: Got the slug from the place, so we can attach the review to the place object.
def place_review_write(request, slug):
    return HttpResponse('<h1>It works!<h1> <p> Review Write </p>')


# TODO: The slug is from the place, the pk is from the review.
def place_review_edit(request, slug, pk):
    return HttpResponse('<h1> Place review edit </h1>')


# Same here, slug is from the place the pk is from the review.
def place_review_delete(request, slug, pk):
    return HttpResponse('<h1> Place review Delete <h/1>')