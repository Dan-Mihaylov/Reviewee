from django.template import Library


register = Library()


@register.inclusion_tag('partials/browse_place_cards.html')
def browse_place_cards(queryset, request, users_favourites):
    return {
        'places': queryset,
        'request': request,
        'users_favourites': users_favourites,
    }


@register.filter()
def in_users_favourites(place, users_favourites):
    return place in users_favourites