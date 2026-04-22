from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Book, BookImage

# Form for creating and editing Book objects
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }

#Custom formset to validate that exactly one image can be marked as primary.
class BaseBookImageFormSet(BaseInlineFormSet):

    # Validation to ensure correct image upload rules
    def clean(self):
        super().clean()
        total_images = 0
        primary_count = 0

        # Loop through each image form
        for form in self.forms:

            # Skip forms without cleaned data (invalid/empty forms)
            if not hasattr(form, "cleaned_data"):
                continue

            # Ignore deleted images
            if form.cleaned_data.get("DELETE"):
                continue

            # Count valid images
            if form.cleaned_data.get("image"):
                total_images += 1

                # Count primary images
                if form.cleaned_data.get("is_primary"):
                    primary_count += 1
        if total_images < 1:
            raise ValidationError("You must upload at least ONE image.")
        if primary_count == 0:
            raise ValidationError("Please choose a primary image.")
        if primary_count > 1:
            raise ValidationError("Only 1 primary image is allowed.")

# Inline formset linking Book with multiple BookImage instances
BookImageFormSet = inlineformset_factory(
    Book,
    BookImage,
    formset=BaseBookImageFormSet,
    fields=("image", "is_primary"),
    extra=1,
    can_delete=True
)