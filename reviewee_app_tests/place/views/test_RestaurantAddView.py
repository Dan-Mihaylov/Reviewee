from reviewee_app_tests.helpers.restaurant_helpers import get_restaurant_data_for_post_form
from reviewee_app_tests.helpers.account_helpers import create_user, create_owner_profile


from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class RestaurantAddViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test__get_user_not_authenticated__expect_redirect_to_login(self):
        expected_url = reverse('login') + '?next=/place/add/restaurant/'

        response = self.client.get(reverse('restaurant add'))

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, expected_url)

    def test__get_user_authenticated_but_not_owner__expect_handle_no_permission(self):
        user = create_user()
        self.client.force_login(user)

        response = self.client.get(reverse('restaurant add'))

        self.assertEqual(403, response.status_code)

    def test__get_user_authenticated_and_owner__expect_status_code_200_and_correct_html(self):
        user = create_user()
        create_owner_profile(user)
        self.client.force_login(user)

        response = self.client.get(reverse('restaurant add'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'place/restaurant-add.html')

    def test__post_user_authenticated_not_owner__expect_handle_no_permissions(self):

        user = create_user()
        self.client.force_login(user)

        response = self.client.post(reverse('restaurant add'), data=get_restaurant_data_for_post_form())
        self.assertEqual(403, response.status_code)
