from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
import re

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # username length validation
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) > 50:
            raise ValidationError("Username must be 50 characters or less.")
        return username

    # email format validation
    def clean_email(self):
        email = self.cleaned_data.get("email")
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format.")
        return email

    # password match validation
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 != p2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone']