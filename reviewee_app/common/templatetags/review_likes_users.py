from django.db.models import QuerySet
from django.template import Library


register = Library()


@register.filter()
def review_likes_users(likes: QuerySet) -> list:
    users = [like_obj.user for like_obj in likes]
    return users

