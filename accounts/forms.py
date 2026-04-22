from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
import re

# Custom user creation form with additional fields and validation
class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=50)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=50)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Validation for username, email format, and password match
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if not username or not email or not p1 or not p2:
            raise ValidationError("Fill out all fields")
        email_valid = re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)
        passwords_match = p1 == p2
        if not email_valid and not passwords_match:
            raise ValidationError("Please input correct information")
        elif not email_valid:
            raise ValidationError("Wrong email format")
        elif not passwords_match:
            raise ValidationError("Passwords need to match")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return cleaned_data

    # Save User with hashed password
    def save(self, commit=True):
        user = super().save(commit=False)
        # Set hashed password
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Profile form for updating address and phone
class ProfileForm(forms.ModelForm):
    address = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=10, required=False)
    class Meta:
        model = Profile
        fields = ['address', 'phone']
    # Server-side validation for phone number format
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            if not re.fullmatch(r"\d{10}", phone):
                raise ValidationError("Enter a valid 10-digit phone number")
        return phone
    
    