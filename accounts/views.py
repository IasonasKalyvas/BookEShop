from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile
from django.http import JsonResponse
from books.models import Book, Category
from .models import UserActivity
from .utils import is_manager, is_admin
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from books.forms import BookForm  # you will need this form
from django.shortcuts import redirect


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


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def register_view(request):
    error_message = None

    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # ✅ IMPORTANT CHANGE (YOUR REQUIREMENT)
            return redirect('accounts:login')

        else:
            # ✅ Get ONLY our custom validation message
            if '__all__' in form.errors:
                error_message = form.errors['__all__'][0]
            else:
                # fallback (e.g username already exists)
                first_field = list(form.errors.keys())[0]
                error_message = form.errors[first_field][0]

    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'error_message': error_message
    })


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

@login_required
def toggle_wishlist(request, book_id):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    book = Book.objects.get(id=book_id)

    if book in profile.favorite_books.all():
        profile.favorite_books.remove(book)

        UserActivity.objects.create(
            user=request.user,
            action='wishlist_remove',
            book=book
        )

        return JsonResponse({'status': 'removed'})
    else:
        profile.favorite_books.add(book)

        UserActivity.objects.create(
            user=request.user,
            action='wishlist_add',
            book=book
        )

        return JsonResponse({'status': 'added'})
    

@login_required
def dashboard(request):
    user = request.user

    if is_admin(user):
        return redirect('accounts:manage_categories')  

    if is_manager(user):
        return redirect('accounts:manage_books')

    return redirect('accounts:profile')   


def manager_required(user):
    return user.is_superuser or user.groups.filter(name="manager").exists()


@user_passes_test(manager_required)
def manage_books(request):
    query = request.GET.get("q")

    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query)

    # 👇 NEW: out of stock books
    out_of_stock_books = Book.objects.filter(stock=0)

    return render(request, "accounts/manage_books.html", {
        "books": books,
        "out_of_stock_books": out_of_stock_books,
        "query": query
    })

@user_passes_test(manager_required)
def manage_users(request):
    users = User.objects.all()

    for u in users:
        if u.is_superuser:
            u.role = "Admin"
        elif u.groups.filter(name="manager").exists():
            u.role = "Manager"
        else:
            u.role = "User"   # ✅ FIX: default role

    return render(request, "accounts/manage_users.html", {
        "users": users
    })


@user_passes_test(manager_required)
def promote_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # ❌ cannot change yourself
    if user == request.user:
        return redirect("accounts:manage_users")

    # ❌ never touch admin
    if user.is_superuser:
        return redirect("accounts:manage_users")

    manager_group = Group.objects.get(name="manager")

    user.groups.clear()
    user.groups.add(manager_group)

    return redirect("accounts:manage_users")


@user_passes_test(manager_required)
def demote_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # ❌ cannot change yourself
    if user == request.user:
        return redirect("accounts:manage_users")

    # ❌ never touch admin
    if user.is_superuser:
        return redirect("accounts:manage_users")

    manager_group = Group.objects.get(name="manager")

    user.groups.remove(manager_group)

    return redirect("accounts:manage_users")


@user_passes_test(manager_required)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:manage_books")
    else:
        form = BookForm()

    return render(request, "accounts/book_form.html", {"form": form})

@user_passes_test(manager_required)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("accounts:manage_books")
    else:
        form = BookForm(instance=book)

    return render(request, "accounts/book_form.html", {"form": form})

@user_passes_test(manager_required)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("accounts:manage_books")

def manage_categories(request):
    categories = Category.objects.all()
    return render(request, "accounts/manage_categories.html", {
        "categories": categories
    })


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Admin cannot delete themselves (optional safety)
    if user == request.user:
        return redirect("accounts:manage_users")

    user.delete()
    return redirect("accounts:manage_users")