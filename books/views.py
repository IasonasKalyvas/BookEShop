from django.shortcuts import render, get_object_or_404
from .models import Book, Category
from django.utils import timezone 
import random

def get_categories():
    """
    Helper function:
    Always fetch categories so filters are ALWAYS visible
    """
    return Category.objects.all()


def book_list(request):
    """
    Show all books (default page)
    Also handles selected filters so UI stays consistent
    """

    books = Book.objects.filter(stock__gt=0)
    selected_genres = request.GET.getlist('genre')
    selected_date = request.GET.get('date_filter')
    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': get_categories(),
        'selected_genres': selected_genres,
        'selected_date': selected_date
    })


def book_detail(request, slug):
    """
    Show single book + recommendations
    """

    book = get_object_or_404(Book, slug=slug)
    similar_books = Book.objects.filter(
        categories__in=book.categories.all()
    ).exclude(id=book.id).distinct()[:4]
    return render(request, 'books/book_detail.html', {
        'book': book,
        'similar_books': similar_books
    })


def book_search(request):
    """
    Search by title OR author
    """

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


def book_filter(request):
    """
    Advanced filtering system:
    - title
    - author
    - id
    - price range
    - date
    - categories
    """

    books = Book.objects.filter(stock__gt=0)
    selected_genres = request.GET.getlist('genre')
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
    elif selected_date == "365":
        books = books.filter(published_date__gte=today - timedelta(days=365))
    if selected_genres:
        for genre in selected_genres:
            books = books.filter(categories__name=genre)

    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': get_categories(),
        'selected_genres': selected_genres,
        'selected_date': selected_date
    })

def featured_books(request):
    """
    Select ONE random book per day
    """

    books = Book.objects.filter(stock__gt=0)
    if books.exists():
        featured = random.choice(list(books))
    else:
        featured = None
    return render(request, 'books/featured.html', {
        'book': featured
    })

def out_of_stock(request):
    """
    Show books that are out of stock
    """

    books = Book.objects.filter(stock=0)
    return render(request, 'books/out_of_stock.html', {'books': books})