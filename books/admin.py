from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Category, BookImage


# ========================= MODIFIED INLINE FORMSET =========================
# Custom formset to validate that exactly one primary image is selected
class BookImageInlineFormSet(forms.BaseInlineFormSet):
    """
    Custom formset that validates only one image can be marked as primary.
    This validation runs when the admin saves the book with images.
    """
    def clean(self):
        super().clean()
        
        # Count how many images are marked as primary
        primary_count = 0
        has_images = False
        
        for form in self.forms:
            # Skip deleted forms and empty forms
            if form.cleaned_data.get('DELETE', False):
                continue
            if not form.cleaned_data.get('image'):
                continue
                
            has_images = True
            if form.cleaned_data.get('is_primary', False):
                primary_count += 1
        
        # Validation: If there are images, exactly one must be primary
        if has_images and primary_count == 0:
            raise ValidationError(
                "You must select exactly ONE primary image. "
                "Please check the 'Is primary' checkbox for one image."
            )
        
        if primary_count > 1:
            raise ValidationError(
                f"Only ONE image can be marked as primary. "
                f"You have selected {primary_count} primary images. "
                "Please uncheck extra primary images."
            )


class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1
    # ========================= ADDED FORMSET =========================
    # Use our custom formset for validation
    formset = BookImageInlineFormSet


class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if not categories:
            raise forms.ValidationError("Select at least ONE category.")
        return categories


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ('title', 'author', 'price', 'stock')
    filter_horizontal = ('categories',)
    inlines = [BookImageInline]
    readonly_fields = ('slug',)
    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "author", "description", "categories",)
        }),
        ("Pricing & Stock", {
            "fields": ("price", "stock")
        }),
        ("Publication", {
            "fields": ("published_date",)
        }),
        ("Book Details", {
            "fields": (
                "isbn_10",
                "isbn_13",
                "publisher",
                "page_count",
                "cover_type"
            )
        }),
        ("System", {
            "fields": ("slug",)
        }),
    )
