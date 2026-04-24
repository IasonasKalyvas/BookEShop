from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Book, Category
from accounts.models import Profile
import re
from decimal import Decimal, InvalidOperation
from django.db import IntegrityError

# Helper function to get all categories for use in multiple views
def get_categories():
    return Category.objects.all()

# Displays all categories available in the system
@login_required
def category_list(request):
    categories = Category.objects.all()

    return render(request, "books/manage_categories.html", {
        "categories": categories
    })

# Add category view that allows logged-in users to create new book categories, ensuring that the category name is unique and not empty
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            try:
                Category.objects.create(name=name)

            except IntegrityError:
                # category already exists → just ignore or handle safely
                pass

        return redirect("books:category_list")

    return redirect("books:category_list")

# Edit category view that allows updating the name of an existing category, ensuring that the new name is not empty and does not duplicate another category's name
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            category.name = name
            category.save()
        return redirect("books:category_list")
    return redirect("books:category_list")

# Delete category view that removes a category and redirects back to the category list page, ensuring that any books associated with the deleted category are not affected (books will simply lose that category association)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("books:category_list")

# List view that displays all books with pagination and filtering options, including genre and publication date filters
def book_list(request):
    books = Book.objects.filter(stock__gt=0)
    search = request.GET.get("search")
    author = request.GET.get("author")
    isbn_13 = request.GET.get("id")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if author:
        if not re.match(r'^[a-zA-Z\s]+$', author):
            author = None
    if isbn_13:
        if not re.match(r'^\d{13}$', isbn_13):
            isbn_13 = None
    def is_valid_price(value):
        try:
            Decimal(value)
            return True
        except (InvalidOperation, TypeError):
            return False
    if min_price and not is_valid_price(min_price):
        min_price = None
    if max_price and not is_valid_price(max_price):
        max_price = None
    if search:
        books = books.filter(title__icontains=search)
    if author:
        books = books.filter(author__icontains=author)
    if isbn_13:
        books = books.filter(isbn_13=isbn_13)
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)
    selected_genres = request.GET.getlist('genre')
    selected_date = request.GET.get('date_filter')
    if selected_genres:
        books = books.filter(categories__name__in=selected_genres).distinct()
    if selected_date:
        from datetime import date, timedelta
        today = date.today()
        if selected_date == "30":
            books = books.filter(published_date__gte=today - timedelta(days=30))
        elif selected_date == "90":
            books = books.filter(published_date__gte=today - timedelta(days=90))
        elif selected_date == "180":
            books = books.filter(published_date__gte=today - timedelta(days=180))
    paginator = Paginator(books, 15)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "books/book_list.html", {
        "books": page_obj,
        "categories": get_categories(),
        "selected_genres": selected_genres,
        "selected_date": selected_date,
        "page_obj": page_obj
    })

# View to display detailed information about a single book, including similar books and wishlist status
def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    is_wishlisted = False
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        is_wishlisted = profile.favorite_books.filter(id=book.id).exists()
    similar_books = Book.objects.filter(
        categories__in=book.categories.all(),
        stock__gt=0
    ).exclude(id=book.id).distinct()[:4]
    return render(request, 'books/book_detail.html', {
    'book': book,
    'similar_books': similar_books,
    'is_wishlisted': is_wishlisted
})

# Searches books by title or author and optionally applies genre/date filters
def book_search(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query) | \
                Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    selected_genres = request.GET.getlist('genre')
    selected_date = request.GET.get('date_filter')
    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': get_categories(),
        'selected_genres': selected_genres,
        'selected_date': selected_date
    })

# Applies multiple filtering rules to books including genre, price, author, and publication date
def book_filter(request):
    books = Book.objects.filter(stock__gt=0)
    selected_genres = request.GET.getlist('genre')
    single_genre = request.GET.get('genre')
    selected_date = request.GET.get('date_filter')
    search = request.GET.get('search')
    if search:
        books = books.filter(title__icontains=search)
    author = request.GET.get('author')
    if author:
        books = books.filter(author__icontains=author)
    book_id = request.GET.get('id')
    if book_id:
        books = books.filter(id=book_id)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)
    from datetime import date, timedelta
    today = date.today()
    if selected_date == "30":
        books = books.filter(published_date__gte=today - timedelta(days=30))
    elif selected_date == "90":
        books = books.filter(published_date__gte=today - timedelta(days=90))
    elif selected_date == "180":
        books = books.filter(published_date__gte=today - timedelta(days=180))
    else:
        pass
    # CASE 1: homepage sends single genre
    if single_genre:
        books = books.filter(categories__name__iexact=single_genre)

    # CASE 2: filter page sends multiple genres
    if selected_genres:
        books = books.filter(categories__name__in=selected_genres).distinct()
    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': get_categories(),
        'selected_genres': selected_genres,
        'selected_date': selected_date
    })

# Displays all books that are currently out of stock
def out_of_stock(request):
    books = Book.objects.filter(stock=0)
    return render(request, 'books/out_of_stock.html', {'books': books})
