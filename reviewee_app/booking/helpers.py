import random
from itertools import chain

from django.db.models import Case, When, Value, Q, F, QuerySet

from django.utils import timezone

from reviewee_app.booking.models import RestaurantBooking, HotelBooking
from reviewee_app.place.models import Hotel, Restaurant


def find_all_bookings_for_place(place: Hotel or Restaurant, filter_by='active', order_by=None) -> QuerySet:

    filter_options = {
        'active': Q(active=True),
        'inactive': Q(active=False),
        'canceled': Q(canceled=True),
    }

    filter_query = filter_options[filter_by] if filter_by in filter_options else None

    order_by_options = {
        '-date',
        'date',
        'created_at',
        '-created_at'
    }

    if filter_query and order_by in order_by_options:
        bookings = place.bookings.filter(filter_query).order_by(order_by)

    elif filter_query and order_by not in order_by_options:
        bookings = place.bookings.filter(filter_query).order_by('-date')

    else:
        bookings = place.bookings.all().order_by('-date')

    update_active_bookings(bookings)

    return bookings


def filter_place_bookings_for_date(bookings: QuerySet, date: str) -> QuerySet:
    result = bookings.filter(date=date)
    return result


def update_active_bookings(bookings) -> None:

    """
    Checks whether the booking date is in the past or the booking is cancelled and if it is, updates the active to False
    :param bookings: QuerySet
    :return: None
    """

    bookings.update(
        active=Case(
            When(Q(date__lt=timezone.localdate()) | Q(canceled=True), then=Value(False)),
            default=Value(True)
        )
    )

    return


def order_bookings(bookings, order_by) -> list:

    """
    Created the functions to optimize the ordering process.
    :param bookings: list
    :param order_by: str
    :return: list
    """

    def order_by_created_at_desc():
        return list(sorted(bookings, reverse=True, key=lambda x: x.date))

    def order_by_created_asc():
        return list(sorted(bookings, key=lambda x: x.date))

    options = {
        '-date': order_by_created_at_desc,
        'date': order_by_created_asc,
    }

    if order_by in options:
        return options[order_by]()

    return bookings


def find_all_bookings_from_search_data(search: str, option: str, order_by='-date') -> list:

    if search is None:
        return []

    options = {
        'active': Q(active=True),
        'inactive': Q(active=False),
    }

    if option in options:
        query = (Q(email__iexact=search) | Q(confirmation_code__exact=search)) & options[option]
    else:
        query = Q(email__iexact=search) | Q(confirmation_code__exact=search)

    restaurant_bookings = RestaurantBooking.objects.filter(query)
    hotel_bookings = HotelBooking.objects.filter(query)

    for bookings in (restaurant_bookings, hotel_bookings):
        update_active_bookings(bookings)

    all_bookings = list(chain(restaurant_bookings, hotel_bookings))
    all_bookings = order_bookings(all_bookings, order_by)

    return all_bookings
