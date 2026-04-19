from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review


def review_page(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:review_page')
    else:
        form = ReviewForm()

    reviews = Review.objects.select_related('book').order_by('-created_at')

    return render(request, 'reviews/review_page.html', {
        'form': form,
        'reviews': reviews
    })