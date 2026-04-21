from django.contrib.auth.models import Group
from .models import UserActivity


def is_manager(user):
    return user.is_authenticated and (
        user.groups.filter(name="manager").exists()
        or user.is_superuser
    )

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def log_activity(user, action, book=None):
    if user.is_authenticated:
        UserActivity.objects.create(
            user=user,
            action=action,
            book=book
        )