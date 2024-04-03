from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views import generic as views

from reviewee_app.place.models import Restaurant, Hotel
from .helpers import get_users_favourite_places
from .models import FavouriteHotel, FavouriteRestaurant


UserModel = get_user_model()


def favourite_functionality(request, place_slug: str, user_pk: int):

    # slug --> <PlaceName-PlacePk-PlaceType>
    available_place_types = {
        'restaurant': Restaurant,
        'hotel': Hotel,
    }

    place_type = place_slug.split('-')[-1]
    place = (available_place_types[place_type]
             .objects.prefetch_related('favourite_to_users')
             .get(slug=place_slug))

    user = get_object_or_404(UserModel, pk=user_pk)
    users_favourite_instance = place.favourite_to_users.filter(user=user)

    if users_favourite_instance.exists():
        users_favourite_instance.first().delete()

    else:

        if place_type == 'hotel':
            FavouriteHotel.objects.create(user=user, hotel=place)
        elif place_type == 'restaurant':
            FavouriteRestaurant.objects.create(user=user, restaurant=place)

    refer_to = request.META.get('HTTP_REFERER') + f'#{place_slug}'
    # Avoid problem with ?page= 'number that doesn't exist'
    redirect_to_list = refer_to.split('?page')
    redirect_to_url = redirect_to_list[0]

    return redirect(redirect_to_url)


# Model-Action-View
class FavouritePlacesListView(LoginRequiredMixin, views.ListView):

    template_name = 'favourite/favourite-places-list.html'
    paginate_by = 2

    def get_queryset(self):
        favourite_places = get_users_favourite_places(self.request.user)
        return favourite_places
