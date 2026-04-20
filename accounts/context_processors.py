def role_flags(request):
    user = request.user

    if not user.is_authenticated:
        return {}

    return {
        "is_manager": user.groups.filter(name="manager").exists() or user.is_superuser,
        "is_admin": user.is_superuser,
    }