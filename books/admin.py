from django.contrib import admin
from django import forms
from .models import Book, Category

class BookAdminForm(forms.ModelForm):
    """
    Custom validation:
    Ensure at least ONE category is selected
    """
    class Meta:
        model = Book
        fields = '__all__'

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if not categories:
            raise forms.ValidationError("You must select at least ONE category.")
        return categories

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ('title', 'author', 'price', 'stock')
    prepopulated_fields = {'slug': ('title',)}
    # Checkbox UI for categories
    filter_horizontal = ('categories',)