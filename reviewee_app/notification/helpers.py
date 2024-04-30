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


def create_notification_on_review_write(
        review: HotelReview or RestaurantReview,
        place: Restaurant or Hotel,
        from_user: UserModel,
) -> None:

    text = f'User {review.user.profile.get_name} has reviewed {place.name} with a rating of {review.rating}/5'
    url_sufix = reverse('place details', kwargs={'slug': place.slug}) + f'#{review.pk}'

    Notification.objects.create(
        user=place.owner,
        text=text,
        url_sufix=url_sufix,
        type='Reviews',
        notification_from_user=from_user
    )

    return


def create_notification_on_review_like(
        review: HotelReview or RestaurantReview,
        user: UserModel,
        from_user: UserModel
) -> None:

    place = review.hotel if hasattr(review, 'hotel') else review.restaurant

    text = f'User {user.profile.get_name} liked your {review.rating}/5 star review for {place.name}.'
    notification_for_user = review.user
    url_sufix = reverse('place details', kwargs={'slug': place.slug}) + f'#{review.pk}'

    Notification.objects.create(
        text=text,
        user=notification_for_user,
        url_sufix=url_sufix,
        type='Likes',
        notification_from_user=from_user,
    )

    return


def remove_notification_on_review_like(review: HotelReview or RestaurantReview, user: UserModel) -> None:

    place = review.hotel if hasattr(review, 'hotel') else review.restaurant

    text = f'User {user.profile.get_name} liked your {review.rating}/5 star review for {place.name}.'
    notification_for_user = review.user
    url_sufix = reverse('place details', kwargs={'slug': place.slug}) + f'#{review.pk}'

    notification = Notification.objects.filter(text=text, user=notification_for_user, url_sufix=url_sufix)
    if notification.exists():
        notification.delete()
    return


def create_notification_for_place_booking(place: Restaurant or Hotel, booking: RestaurantBooking or HotelBooking) -> None:
    text = f'{booking.first_name} {booking.last_name} has created a reservation at the {place.name} for the {booking.date}.'
    notification_for_user = place.owner
    url_sufix = reverse('place bookings') + f'?slug={place.slug}'

    Notification.objects.create(text=text, user=notification_for_user, url_sufix=url_sufix, type='Bookings')

    return
