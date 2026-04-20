from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
import re


class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=50)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        # 1️⃣ Missing fields
        if not username or not email or not p1 or not p2:
            raise ValidationError("Fill out all fields")

        # 2️⃣ Email validation
        email_valid = re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

        # 3️⃣ Password match
        passwords_match = p1 == p2

        # 4️⃣ Combined logic
        if not email_valid and not passwords_match:
            raise ValidationError("Please input correct information")

        elif not email_valid:
            raise ValidationError("Wrong email format")

        elif not passwords_match:
            raise ValidationError("Passwords need to match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# ================= PROFILE =================
class ProfileForm(forms.ModelForm):
    address = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=10, required=False)

    class Meta:
        model = Profile
        fields = ['address', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if phone:
            if not re.fullmatch(r"\d{10}", phone):
                raise ValidationError("Enter a valid 10-digit phone number")


        return phone