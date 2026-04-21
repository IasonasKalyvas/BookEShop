from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from books.models import Book
from accounts.utils import log_activity


# Helper function
def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return None

# CART PAGE
def cart_view(request):
    # LOGGED IN
    if request.user.is_authenticated:
        cart = get_cart(request)
        items = cart.items.all()

        return render(request, 'orders/cart.html', {
            'cart': cart,
            'items': items
        })

    # GUEST (unchanged)
    session_cart = request.session.get('cart', {})

    class TempItem:
        def __init__(self, book, quantity):
            self.book = book
            self.quantity = quantity

        def total_price(self):
            return self.book.price * self.quantity

    items = []
    total = 0

    for book_id, qty in session_cart.items():
        book = Book.objects.get(id=book_id)
        item = TempItem(book, qty)
        items.append(item)
        total += item.total_price()

    class TempCart:
        def __init__(self, items, total):
            self._items = items
            self._total = total

        @property
        def items(self):
            return self._items

        def total_price(self):
            return self._total

    cart = TempCart(items, total)

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'items': items
    })

# ADD TO CART
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    qty = int(request.GET.get("qty", 1))

    # ================= LOGGED IN =================
    if request.user.is_authenticated:
        cart = get_cart(request)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book
        )

        if not created:
            item.quantity += qty
        else:
            item.quantity = qty

        item.save()


    # ================= GUEST =================
    else:
        cart = request.session.get('cart', {})

        if str(book_id) in cart:
            cart[str(book_id)] += qty
        else:
            cart[str(book_id)] = qty

        request.session['cart'] = cart

    return redirect('orders:cart')

def remove_from_cart(request, book_id):
    # LOGGED IN USERS
    if request.user.is_authenticated:
        cart = get_cart(request)

        item = CartItem.objects.filter(cart=cart, book_id=book_id).first()

        if item:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()      

    # GUEST USERS
    else:
        cart = request.session.get('cart', {})

        if str(book_id) in cart:
            if cart[str(book_id)] > 1:
                cart[str(book_id)] -= 1
            else:
                del cart[str(book_id)]

        request.session['cart'] = cart

    return redirect('orders:cart')

def checkout(request):

    # ================= GUEST + LOGGED-IN SUPPORT =================
    if request.user.is_authenticated:
        cart = get_cart(request)
        items = cart.items.all()
        total = cart.total_price()

    else:
        session_cart = request.session.get('cart', {})

        if not session_cart:
            messages.error(request, "Your cart is empty.")
            return redirect("orders:cart")

        items = []
        total = 0

        class TempItem:
            def __init__(self, book, quantity):
                self.book = book
                self.quantity = quantity

            def total_price(self):
                return self.book.price * self.quantity

        for book_id, qty in session_cart.items():
            book = Book.objects.get(id=book_id)
            item = TempItem(book, qty)
            items.append(item)
            total += item.total_price()

    # ================= POST (CREATE ORDER) =================
    if request.method == "POST":

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_price=total
        )

        # LOGGED-IN CART
        if request.user.is_authenticated:
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price
                )

                item.book.stock -= item.quantity
                item.book.save()

            cart.items.all().delete()

        # GUEST CART
        else:
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price
                )

                item.book.stock -= item.quantity
                item.book.save()

            request.session['cart'] = {}  # clear guest cart

        messages.success(request, "Order completed!")
        return redirect("home")

    return render(request, "orders/checkout.html", {
    "items": items,
    "total": total,
    "cart_items": items
})