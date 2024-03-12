# Generate the user profile pic path, dynamically
# this function will be called when save() method is called on the Profile Instance

def user_profile_photo_upload_path(instance, filename):

    user_pk = instance.user.pk

    upload_path = f'images/account/{user_pk}/photos/{filename}'

    return upload_path