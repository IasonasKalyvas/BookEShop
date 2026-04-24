from django.shortcuts import render
from django.core.paginator import Paginator
from books.models import Category

def home(request):
    categories_list = Category.objects.all()

    paginator = Paginator(categories_list, 16)
    page_number = request.GET.get("page")
    categories = paginator.get_page(page_number)

    return render(request, 'core/home.html', {
        'categories': categories
    })
