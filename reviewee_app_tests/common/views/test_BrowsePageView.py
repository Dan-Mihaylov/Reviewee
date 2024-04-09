from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from reviewee_app_tests.helpers.hotel_helpers import create_valid_hotel
from reviewee_app_tests.helpers.restaurant_helpers import create_valid_restaurant


UserModel = get_user_model()
VALID_PLACE_COUNT = 3


class BrowsePageViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user('test@mail.com', 'testpass321')

    def test__browse_page_choice_restaurant__expect_display_only_restaurants(self):
        restaurants = [create_valid_restaurant(self.user) for _ in range(VALID_PLACE_COUNT)]
        hotel = create_valid_hotel(self.user)
        url = reverse('browse') + '?place=restaurants'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/browse.html')
        self.assertCountEqual(response.context['object_list'], restaurants)
        self.assertFalse(hotel in response.context['object_list'])

    def test__browse_page_choice_hotel__expect_display_only_hotels(self):
        restaurant = create_valid_restaurant(self.user)
        hotels = [create_valid_hotel(self.user) for _ in range(VALID_PLACE_COUNT)]
        url = reverse('browse') + '?place=hotels'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/browse.html')
        self.assertCountEqual(response.context['object_list'], hotels)
        self.assertFalse(restaurant in response.context['object_list'])

    def test__browse_page_choice_invalid__expect_raiseHttp404(self):
        url = reverse('browse') + '?place=invalid'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
