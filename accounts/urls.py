from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),  # ✅ NEW
    path('wishlist/toggle/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/books/', views.manage_books, name='manage_books'),
    path('dashboard/users/', views.manage_users, name='manage_users'),
    path('dashboard/users/promote/<int:user_id>/', views.promote_user, name='promote_user'),
    path('dashboard/users/demote/<int:user_id>/', views.demote_user, name='demote_user'),
    path('dashboard/books/add/', views.add_book, name='add_book'),
    path('dashboard/books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('dashboard/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('dashboard/categories/', views.manage_categories, name='manage_categories'),
]