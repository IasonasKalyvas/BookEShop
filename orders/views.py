from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from books.models import Book

# Helper function
def get_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

# CART PAGE
def cart_view(request):
    cart = get_cart(request.user)
    items = cart.items.all()
    return render(request, 'orders/cart.html', {
        'cart': cart,
        'items': items
    })

# ADD TO CART
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = get_cart(request.user)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book
    )
    qty = int(request.GET.get("qty", 1))
    if not created:
        item.quantity += qty    
    else:
        item.quantity = qty
    item.save()
    return redirect('orders:cart')

# REMOVE FROM CART
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('orders:cart')

def checkout(request):
    cart = get_cart(request.user)
    if cart.total_price() <= 0:
        messages.error(request, "Your cart is empty.")
        return redirect("orders:cart")
    if request.method == "POST":
        # CREATE ORDER
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price()
        )
        for item in cart.items.all():
            # CREATE ORDER ITEM
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            # REDUCE STOCK
            item.book.stock -= item.quantity
            item.book.save()
        # CLEAR CART AFTER EVERYTHING
        cart.items.all().delete()
        messages.success(request, "Order completed!")
        return redirect("home")  # or wherever you want
    return render(request, "orders/checkout.html", {
        "cart": cart
    })