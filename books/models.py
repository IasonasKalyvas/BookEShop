from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date

class Category(models.Model):
    """
    Book category (Horror, Action, etc.)
    Created once and reused via admin
    """

    name = models.CharField(max_length=100, unique=True)

    class Meta:
     verbose_name = "Category"
     verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Main Book model
    """

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999)
        ]
    )
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateField(null=True, blank=True)

    def clean(self):
        """
        Validate published_date:
        - Cannot be in the future
        """

        if self.published_date:
            today = date.today()
            if self.published_date > today:
             raise ValidationError({
                  "published_date": "Publication date cannot be in the future."
                })
            if self.published_date.year < today.year - 100:
                raise ValidationError({
                    "published_date": "Publication date is too old."
             })

    def save(self, *args, **kwargs):
        """
        Auto-generate slug from title
        """

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title