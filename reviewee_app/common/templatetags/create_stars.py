from django.template import Library


register = Library()


@register.inclusion_tag('partials/create-stars.html')
def create_stars(place):

    available_stars = 5

    place_rating = place.rating()
    full_stars = range(int(place_rating))
    half_star = (place_rating - int(place_rating)) >= 0.5
    empty_stars = range(available_stars - int(place_rating) - half_star)

    return {
        'full_stars': full_stars,
        'half_star': half_star,
        'empty_stars': empty_stars,
    }


# TODO: do it abstract, don't DRY
@register.inclusion_tag('partials/create-stars.html')
def create_stars_for_review(review):

    available_stars = 5

    review_rating = review.rating
    full_stars = range(int(review_rating))
    half_stars = (review_rating - int(review_rating)) >= 0.5
    empty_stars = range(available_stars - int(review_rating) - half_stars)

    return {
        'full_stars': full_stars,
        'half_star': half_stars,
        'empty_stars': empty_stars,
    }