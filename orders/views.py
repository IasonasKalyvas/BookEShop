from profile import Profile
from accounts.models import Profile
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from books.models import Book

# Helper function to get or create cart for authenticated users
def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return None

# Cart view to display current cart items and total price for both logged-in and guest users, using session data for guests and database for authenticated users
def cart_view(request):
    if request.user.is_authenticated:
        cart = get_cart(request)
        items = cart.items.all()
        return render(request, 'orders/cart.html', {
            'cart': cart,
            'items': items
        })
    session_cart = request.session.get('cart', {})

    # Temporary item class to mimic CartItem for guests
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

        # Manually calculate total for guest cart session
        total += item.total_price()

    # Wrapper object to simulate Cart model behavior for guest users    
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

# Add to cart view to handle both logged-in and guest users, updating database or session accordingly, and redirecting to cart page after adding
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    qty = int(request.GET.get("qty", 1))

    # Logged-in users: add to CartItem in database
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

    # Guest users
    else:
        cart = request.session.get('cart', {})
        if str(book_id) in cart:
            cart[str(book_id)] += qty
        else:
            cart[str(book_id)] = qty
        request.session['cart'] = cart
    return redirect('orders:cart')

# Remove from cart view to decrease quantity or remove item for both logged-in and guest users, updating database or session accordingly
def remove_from_cart(request, book_id):
    if request.user.is_authenticated:
        cart = get_cart(request)
        item = CartItem.objects.filter(cart=cart, book_id=book_id).first()
        if item:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()      
    else:
        cart = request.session.get('cart', {})
        if str(book_id) in cart:
            if cart[str(book_id)] > 1:
                cart[str(book_id)] -= 1
            else:
                del cart[str(book_id)]
        request.session['cart'] = cart
    return redirect('orders:cart')

# checkout view to process orders for both logged-in and guest users, creating Order and OrderItem records, updating stock, and clearing carts after purchase
def checkout(request):
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

        #Temporary item class to mimic CartItem for guests
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

    # Order processing on POST
    if request.method == "POST":
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_price=total
        )
        if request.user.is_authenticated:
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price
                )

                # Reduce stock after successful purchase
                item.book.stock -= item.quantity
                item.book.save()

                # Remove purchased books from user's favorites if they exist there
                profile, _ = Profile.objects.get_or_create(user=request.user)
                profile.favorite_books.remove(item.book)

            # Clear user's cart after purchase    
            cart.items.all().delete()
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

            # Clear guest cart session after purchase    
            request.session['cart'] = {}  
        messages.success(request, "Order completed!")
        return redirect("home")
    return render(request, "orders/checkout.html", {
    "items": items,
    "total": total,
    "cart_items": items
})