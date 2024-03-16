# Because we have a few place models and DRY
def find_place_object_for_user(user, slug):
    if user.restaurants.filter(slug=slug).exists():
        return user.restaurants.get(slug=slug)
    else:
        return user.hotels.get(slug=slug)