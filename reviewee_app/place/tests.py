from django.contrib.auth import get_user_model
from . import models
from django.test import TestCase


UserModel = get_user_model()


class UserAccessesPlacesCorrectly(TestCase):

    def setUp(self) -> None:
        self.user = UserModel.objects.get(id=1)

    def test__user_accesses_hotels(self):
        hotels = models.Hotel.objects.all()
        user_hotels = self.user.hotels.all()

        self.assertEquals(hotels, user_hotels)




