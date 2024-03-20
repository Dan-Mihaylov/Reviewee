from django.core.files.storage import default_storage

# Generate the user profile pic path, dynamically
# this function will be called when save() method is called on the Profile Instance


def user_profile_photo_upload_path(instance, filename):

    user_pk = instance.user.pk
    suffix = filename.split('.')[-1]

    upload_path = f'images/account/{user_pk}/photos/profile_picture.{suffix}'

    if default_storage.exists(upload_path):
        default_storage.delete(upload_path)

    return upload_path
