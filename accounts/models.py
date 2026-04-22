from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    # Wishlist system 
    favorite_books = models.ManyToManyField(
        Book,
        blank=True,
        related_name='favored_by'
    )
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.user.username