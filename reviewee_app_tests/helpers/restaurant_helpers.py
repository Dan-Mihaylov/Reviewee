from django.contrib.auth import get_user_model

from reviewee_app.place.models import Restaurant


UserModel = get_user_model()


def get_correct_restaurant_data(user: UserModel) -> dict:
    data = {
        'name': 'test name',
        'photo': './image.jpg',
        'description': 'test description',
        'owner': user,
        'country': 'United States',
        'city': 'United States',
        'address': 'United States',
        'post_code': '12345',
        'opening_time': '10:00:00',
        'closing_time': '22:00:00',
        'available_seats': 30,
    }
    return data


def get_restaurant_data_for_post_form():
    data = {
        'name': 'test name',
        'photo': './image.jpg',
        'description': 'test description',
        'opening_time': '10:00:00',
        'closing_time': '22:00:00',
        'available_seats': 30,
        'country': 'United States',
        'city': 'Test City',
        'address': 'Test Address',
        'post_code': '12345',
    }
    return data


def create_valid_restaurant(user: UserModel) -> Restaurant:
    restaurant = Restaurant(**get_correct_restaurant_data(user))
    restaurant.save()
    return restaurant
