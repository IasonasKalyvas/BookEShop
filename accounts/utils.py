from django.contrib.auth.models import Group

def is_manager(user):
    return user.is_authenticated and (
        user.groups.filter(name="manager").exists()
        or user.is_superuser
    )

def is_admin(user):
    return user.is_authenticated and user.is_superuser