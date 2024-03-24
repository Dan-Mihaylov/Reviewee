from django.template import Library


register = Library()


@register.inclusion_tag('partials/browse_place_cards.html')
def browse_place_cards(queryset, request):
    return {
        'places': queryset,
        'request': request
    }
