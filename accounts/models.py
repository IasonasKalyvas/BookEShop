from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # future features
    favorite_books = models.ManyToManyField('books.Book', blank=True)

    def __str__(self):
        return self.user.username
    

class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('add_cart', 'Added to Cart'),
        ('remove_cart', 'Removed from Cart'),
        ('checkout', 'Checkout'),
        ('wishlist_add', 'Added to Wishlist'),
        ('wishlist_remove', 'Removed from Wishlist'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"    
    

    