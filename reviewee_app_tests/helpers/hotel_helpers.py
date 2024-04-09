from django.contrib.auth import get_user_model

from reviewee_app.place.models import Hotel


UserModel = get_user_model()


def create_valid_hotel(user: UserModel):

    hotel = Hotel(
        name='test name',
        photo='./image.jpg',
        description='test description',
        owner=user,
        country='United States',
        city='United States',
        address='United States',
        post_code='12345',
        check_in_time='13:00:00',
        check_out_time='10:00:00',
        available_rooms=30,
    )
    hotel.save()
    return hotel
