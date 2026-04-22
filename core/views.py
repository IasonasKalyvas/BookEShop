from django.shortcuts import render
from books.models import Category

def home(request):
    # Get all available categories
    categories = Category.objects.all()
    return render(request, 'core/home.html', {
        'categories': categories
    })