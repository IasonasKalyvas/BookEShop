from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.views import manager_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404

# Review page view that allows users to submit reviews for books and displays existing reviews with pagination, ensuring that the form is properly validated and that reviews are displayed in a user-friendly manner
def review_page(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:review_page')
    else:
        form = ReviewForm()
    reviews_list = Review.objects.select_related('book').order_by('-created_at')
    paginator = Paginator(reviews_list, 15)
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    return render(request, 'reviews/review_page.html', {
        'form': form,
        'reviews': reviews
    })

# Manage reviews view that allows superusers to view and search through all reviews, with pagination and search functionality based on reviewer's first or last name, ensuring that only authorized users can access this page
@user_passes_test(lambda u: u.is_superuser)
def manage_reviews(request):
    query = request.GET.get("q")
    reviews = Review.objects.select_related('book').order_by('-created_at')

    # Search by first or last name
    if query:
        reviews = reviews.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    return render(request, 'reviews/manage_reviews.html', {
        'reviews': reviews,
        'query': query
    })

# Delete review view that allows superusers to delete inappropriate reviews, ensuring that only authorized users can perform this action and redirecting back to the manage reviews page after deletion
@user_passes_test(lambda u: u.is_superuser)
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('reviews:manage_reviews')