from django import forms
from .models import Review
from books.models import Book

# Review form for users to submit their reviews on books
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'first_name', 'last_name', 'rating', 'comment']

    # Custom form fields with validation
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'maxlength': 300,
        'rows': 4,
        'placeholder': 'Write your review (max 300 characters)...'
    }))

    # Dropdown to select the book being reviewed
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        empty_label="Select a book"
    )