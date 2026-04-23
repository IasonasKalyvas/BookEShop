from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile
from .utils import is_manager, is_admin
from books.models import Book
from books.forms import BookForm, BookImageFormSet 

# Account views: login, logout, register, profile, wishlist toggle, dashboard redirection, and management views for books and users.
def login_view(request):
    error_message = None
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profile')
        else:
            error_message = "Wrong username or password"
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'error_message': error_message
    })

# Logs out the current authenticated user and redirects to login page
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

# Handles user registration with validation and redirects to login on success
def register_view(request):
    error_message = None
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        else:
            if '__all__' in form.errors:
                error_message = form.errors['__all__'][0]
            else:
                first_field = list(form.errors.keys())[0]
                error_message = form.errors[first_field][0]
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {
        'form': form,
        'error_message': error_message
    })

# Displays and updates user profile information (address and phone)
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Information Updated Successfully")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile
    })

# Adds or removes a book from the user's wishlist and returns JSON response for AJAX updates
@login_required
def toggle_wishlist(request, book_id):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    book = get_object_or_404(Book, id=book_id)
    if book in profile.favorite_books.all():
        profile.favorite_books.remove(book)
        return JsonResponse({'status': 'removed'})
    else:
        profile.favorite_books.add(book)
        return JsonResponse({'status': 'added'})

# Redirects users to different dashboards based on their role (admin, manager, or regular user)
@login_required
def dashboard(request):
    user = request.user
    if is_admin(user):
        return redirect('accounts:manage_categories')
    if is_manager(user):
        return redirect('accounts:manage_books')
    return redirect('accounts:profile')

# Checks if user has manager or admin privileges for restricted access views
def manager_required(user):
    return user.is_superuser or user.groups.filter(name="manager").exists()

# Displays and filters all books for admin/manager management panel
@user_passes_test(manager_required)
def manage_books(request):
    query = request.GET.get("q")
    books = Book.objects.filter(stock__gt=0)
    if query:
        books = books.filter(title__icontains=query)
    out_of_stock_books = Book.objects.filter(stock=0)
    return render(request, "accounts/manage_books.html", {
        "books": books,
        "out_of_stock_books": out_of_stock_books,
        "query": query
    })

# Handles creation of new books including image uploads using formsets
@user_passes_test(manager_required)
def add_book(request):
    formset = BookImageFormSet(
        request.POST or None,
        request.FILES or None,
        prefix='images'
    )
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid() and formset.is_valid():
            book = form.save()
            formset.instance = book
            formset.save()
            return redirect("accounts:manage_books")
    else:
        form = BookForm()
    return render(request, "accounts/book_form.html", {
        "form": form,
        "formset": formset
    })

# Handles editing existing book details and updating associated images
@user_passes_test(manager_required)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    formset = BookImageFormSet(
        request.POST or None,
        request.FILES or None,
        instance=book,
        prefix='images'
    )
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("accounts:manage_books")
    else:
        form = BookForm(instance=book)
    return render(request, "accounts/book_form.html", {
        "form": form,
        "formset": formset
    })

# Deletes a book from the system permanently
@user_passes_test(manager_required)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("accounts:manage_books")

# Displays all users with assigned roles for admin/manager management panel
@user_passes_test(manager_required)
def manage_users(request):
    users = User.objects.all()
    for u in users:
        if u.is_superuser:
            u.role = "Admin"
        elif u.groups.filter(name="manager").exists():
            u.role = "Manager"
        else:
            u.role = "User"
    return render(request, "accounts/manage_users.html", {
        "users": users
    })

# Promotes a user to manager role by assigning them to the manager group
@user_passes_test(manager_required)
def promote_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user or user.is_superuser:
        return redirect("accounts:manage_users")
    manager_group, _ = Group.objects.get_or_create(name="manager")
    user.groups.clear()
    user.groups.add(manager_group)
    return redirect("accounts:manage_users")

# Removes manager role from a user by clearing group assignment
@user_passes_test(manager_required)
def demote_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user or user.is_superuser:
        return redirect("accounts:manage_users")
    manager_group, _ = Group.objects.get_or_create(name="manager")
    user.groups.remove(manager_group)
    return redirect("accounts:manage_users")

# Deletes a user account except the currently logged-in admin
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        return redirect("accounts:manage_users")
    user.delete()
    return redirect("accounts:manage_users")






