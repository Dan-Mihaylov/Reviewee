from django.test import TestCase
from django.shortcuts import reverse

from reviewee_app.booking.models import HotelBooking
from reviewee_app_tests.helpers.account_helpers import create_user
from reviewee_app_tests.helpers.hotel_helpers import create_valid_hotel
from reviewee_app_tests.helpers.hotel_booking_helpers import create_valid_hotel_booking, valid_hotel_booking_data


class BookingBookHotelTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.hotel = create_valid_hotel(self.user)

    def test__create_valid_hotel_booking__expect_creates_booking(self):
        hotel_bookings_before = HotelBooking.objects.all()

        booking = create_valid_hotel_booking(self.hotel)

        hotel_bookings_after = HotelBooking.objects.all()
        created_booking = HotelBooking.objects.first()

        self.assertNotEqual(hotel_bookings_before, hotel_bookings_after)
        self.assertEqual(booking, created_booking)

    def test__get_with_invalid_hotel_slug__expect_raise_Http404(self):

        response = self.client.get(reverse('book hotel', kwargs={'place_slug': 'invalid'}))

        self.assertEqual(response.status_code, 404)

    def test__get_with_valid_hotel_slug__expect_status_code_200_and_correct_template(self):
        slug = self.hotel.slug

        response = self.client.get(reverse('book hotel', kwargs={'place_slug': slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/book-hotel.html')

    def test__post_with_valid_hotel_data__expect_booking_created_redirects_to_booking_successful(self):

        hotel = create_valid_hotel(self.user)
        slug = hotel.slug
        booking_data = valid_hotel_booking_data(hotel)
        booking_data['hotel'] = hotel.pk

        response = self.client.post(reverse('book hotel', kwargs={'place_slug': slug}), data=booking_data)

        booking = HotelBooking.objects.get(**booking_data)

        self.assertEqual(response.status_code, 302)
        self.assertIn(booking, HotelBooking.objects.all())
        self.assertURLEqual(response.url, reverse('booking successful'))
