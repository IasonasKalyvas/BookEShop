from .models import Cart

# Context processor to add cart item count to all templates
def cart_count(request):
    # For authenticated users, count items in their cart
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return {
            "cart_count": sum(item.quantity for item in cart.items.all())
        }
    # For guests, count items in session cart
    cart = request.session.get('cart', {})
    return {
        "cart_count": sum(int(qty) for qty in cart.values())
    }