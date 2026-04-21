from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review
from reviews.models import Review
from django.core.paginator import Paginator


def review_page(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:review_page')
    else:
        form = ReviewForm()

    reviews_list = Review.objects.select_related('book').order_by('-created_at')

    # ✅ PAGINATION (16 per page)
    paginator = Paginator(reviews_list, 15)
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)

    return render(request, 'reviews/review_page.html', {
        'form': form,
        'reviews': reviews
    })