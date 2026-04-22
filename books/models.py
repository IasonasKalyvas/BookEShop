from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import date

# Category model to organize books into different genres or types
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

# Book model with additional fields and validation for publication date
class Book(models.Model):
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
        validators=[MinValueValidator(0), MaxValueValidator(999)]
    )
    isbn_10 = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message="ISBN-10 must be exactly 10 digits.")]
    )
    isbn_13 = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        validators=[RegexValidator(regex=r'^\d{13}$', message="ISBN-13 must be exactly 13 digits.")]
    )
    publisher = models.CharField(max_length=200, null=True)
    page_count = models.PositiveIntegerField(null=True)
    COVER_CHOICES = [
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
        ('ebook', 'E-book'),
    ]
    cover_type = models.CharField(max_length=20, choices=COVER_CHOICES, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateField(null=True)

    def clean(self):
        if self.published_date:
            today = date.today()
            if self.published_date > today:
                raise ValidationError({"published_date": "Publication date cannot be in the future."})
            if self.published_date.year < today.year - 100:
                raise ValidationError({"published_date": "Publication date is too old."})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # Helper method to get the primary image of the book, or fallback to the first image if no primary is set
    def get_primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        # Fallback to first image if no primary is set
        return self.images.first()

    # Helper method to get all images ordered with primary first, then by id
    def get_ordered_images(self):
        from django.db.models import Case, When, Value, IntegerField
        # Order by is_primary descending (True=1 comes first), then by id
        return self.images.annotate(
            primary_order=Case(
                When(is_primary=True, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('primary_order', 'id')
    def __str__(self):
        return self.title

# New model to handle multiple images per book, with one primary image
class BookImage(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='books/gallery/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    is_primary = models.BooleanField(default=False)

    # Override save method to ensure only one primary image per book
    def save(self, *args, **kwargs):
        # If this image is being set as primary, unset all other primary images for this book
        if self.is_primary:
            BookImage.objects.filter(
                book=self.book,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.book.title} Image"

    class Meta:
        ordering = ['-is_primary', 'id']
