from django.urls import path
from . import views
from books import views as book_views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    # Wishlist toggle
    path('wishlist/toggle/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    #Admin dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/categories/', book_views.category_list, name='manage_categories'),
    path('dashboard/books/', views.manage_books, name='manage_books'),
    path('dashboard/users/', views.manage_users, name='manage_users'),
    path('dashboard/users/promote/<int:user_id>/', views.promote_user, name='promote_user'),
    path('dashboard/users/demote/<int:user_id>/', views.demote_user, name='demote_user'),
    path('dashboard/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('dashboard/books/add/', views.add_book, name='add_book'),
    path('dashboard/books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('dashboard/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]