from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    path('wishlist/toggle/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    # ✅ DASHBOARD ENTRY POINT
    path('dashboard/', views.dashboard, name='dashboard'),

    # ✅ ONLY KEEP THESE 3 PAGES
    path('dashboard/categories/', views.manage_categories, name='manage_categories'),
    path('dashboard/books/', views.manage_books, name='manage_books'),
    path('dashboard/users/', views.manage_users, name='manage_users'),

    # USERS ACTIONS
    path('dashboard/users/promote/<int:user_id>/', views.promote_user, name='promote_user'),
    path('dashboard/users/demote/<int:user_id>/', views.demote_user, name='demote_user'),
    path('dashboard/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    # BOOK ACTIONS
    path('dashboard/books/add/', views.add_book, name='add_book'),
    path('dashboard/books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('dashboard/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]