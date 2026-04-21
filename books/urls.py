from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('search/', views.book_search, name='book_search'),
    path('filter/', views.book_filter, name='book_filter'),
    path('featured/', views.featured_books, name='featured_books'),
    path('out-of-stock/', views.out_of_stock, name='out_of_stock'),

    # ================= CATEGORY ROUTES =================
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # ⚠️ MUST ALWAYS BE LAST
    path('<slug:slug>/', views.book_detail, name='book_detail'),
]