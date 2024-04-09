from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from reviewee_app_tests.helpers.hotel_helpers import create_valid_hotel
from reviewee_app_tests.helpers.restaurant_helpers import create_valid_restaurant


UserModel = get_user_model()


class HomePageViewTestCase(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user('test@mail.com', 'testpass321')

    def test__home_page_when_no_places__expect_200_and_empty_object_list(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/index.html')

    def test__home_page_when_one_restaurant__expect_200_and_one_object_in_object_list(self):
        restaurant = create_valid_restaurant(self.user)
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/index.html')
        self.assertListEqual(response.context['object_list'], [restaurant])

    def test__home_page_when_restaurant_and_hotel_created__displays_both_type_of_objects(self):
        restaurant = create_valid_restaurant(self.user)
        hotel = create_valid_hotel(self.user)
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/index.html')
        self.assertListEqual(response.context['object_list'], [hotel, restaurant])

    def test__home_page_displaying_latest_additions_in_correct_order__expect_objects_ordered_by_latest_additions(self):
        restaurant_1 = create_valid_restaurant(self.user)
        hotel_1 = create_valid_hotel(self.user)
        restaurant_2 = create_valid_restaurant(self.user)
        hotel_2 = create_valid_hotel(self.user)
        response = self.client.get(reverse('home'))

        correct_order = [hotel_2, restaurant_2, hotel_1, restaurant_1]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/index.html')
        self.assertListEqual(response.context['object_list'], correct_order)

