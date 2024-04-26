from .models import Notification
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ..booking.models import RestaurantBooking, HotelBooking
from ..place.models import Restaurant, Hotel
from ..review.models import HotelReview, RestaurantReview

UserModel = get_user_model()


def create_notification_on_register(user: UserModel) -> None:

    text = f'You have successfully registered to Reviewee, explore, review and manage your places'

    Notification.objects.create(user=user, text=text, read=False, type='Account')

    return


def create_notification_on_review_write(review: HotelReview or RestaurantReview, place: Restaurant or Hotel):

    text = f'User {review.user.profile.get_name} has reviewed {place.name} with a rating of {review.rating}/5'
    link = reverse('place details', kwargs={'slug': place.slug}) + f'#{review.pk}'

    Notification.objects.create(user=place.owner, text=text, link=link, type='Reviews')

    return


def create_notification_on_review_like(review: HotelReview or RestaurantReview, user: UserModel) -> None:

    place = review.hotel if hasattr(review, 'hotel') else review.restaurant

    text = f'User {user.profile.get_name} liked your {review.rating}/5 star review for {place.name}.'
    notification_for_user = review.user
    link = reverse('place details', kwargs={'slug': place.slug}) + f'#{review.pk}'

    Notification.objects.create(text=text, user=notification_for_user, link=link, type='Likes')

    return


def remove_notification_on_review_like(review: HotelReview or RestaurantReview, user: UserModel) -> None:

    place = review.hotel if hasattr(review, 'hotel') else review.restaurant

    text = f'User {user.profile.get_name} liked your {review.rating}/5 star review for {place.name}.'
    notification_for_user = review.user
    link = reverse('place details', kwargs={'slug': place.slug}) + f'#{review.pk}'

    notification = Notification.objects.filter(text=text, user=notification_for_user, link=link)
    if notification.exists():
        notification.delete()
    return


def create_notification_for_place_booking(place: Restaurant or Hotel, booking: RestaurantBooking or HotelBooking) -> None:
    text = f'{booking.first_name} {booking.last_name} has created a reservation at the {place.name} for the {booking.date}.'
    notification_for_user = place.owner
    link = reverse('place bookings') + f'?slug={place.slug}'

    Notification.objects.create(text=text, user=notification_for_user, link=link, type='Bookings')

    return
