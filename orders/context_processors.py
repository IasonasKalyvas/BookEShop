from .models import Cart

def cart_count(request):
    # LOGGED IN USERS
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)

        return {
            "cart_count": sum(item.quantity for item in cart.items.all())
        }

    # GUEST USERS
    cart = request.session.get('cart', {})

    return {
        "cart_count": sum(int(qty) for qty in cart.values())
    }