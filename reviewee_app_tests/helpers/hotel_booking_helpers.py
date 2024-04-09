import datetime

from reviewee_app.booking.models import HotelBooking


def valid_hotel_booking_data(hotel) -> dict:

    hotel_data = {
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'email': 'reviewee.app@gmail.com',
        'hotel': hotel,
        'date': datetime.date.today() + datetime.timedelta(days=1),
        'rooms': 1,
        'nights': 3,
    }
    return hotel_data


def create_valid_hotel_booking(hotel) -> HotelBooking:
    hotel_data = valid_hotel_booking_data(hotel)
    hotel_booking = HotelBooking(**hotel_data)
    hotel_booking.save()
    return hotel_booking
