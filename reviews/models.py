from django.db import models
from books.models import Book


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")

    first_name = models.CharField(max_length=50, default="Anonymous")
    last_name = models.CharField(max_length=50, blank=True, default="")

    rating = models.IntegerField(default=5)
    comment = models.TextField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.rating}⭐"