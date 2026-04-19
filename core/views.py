from django.shortcuts import render
from books.models import Category, Book
from reviews.models import Review


def home(request):
    featured_books = Book.objects.order_by('?')[:8]
    categories = Category.objects.all()
    recommended_books = Book.objects.filter(stock__gt=0).order_by('?')[:6]

    # RANDOM REVIEWS (same idea as book detail, but global)
    random_reviews = Review.objects.select_related('book').order_by('?')[:10]

    return render(request, 'core/home.html', {
        'featured_books': featured_books,
        'categories': categories,
        'recommended_books': recommended_books,
        'random_reviews': random_reviews
    })