from django import forms
from .models import Review
from books.models import Book


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'first_name', 'last_name', 'rating', 'comment']

    # Custom fields
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'maxlength': 300,
        'rows': 4,
        'placeholder': 'Write your review (max 300 characters)...'
    }))

    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        empty_label="Select a book"
    )