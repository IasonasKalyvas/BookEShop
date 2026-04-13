from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('search/', views.book_search, name='book_search'),
    path('filter/', views.book_filter, name='book_filter'),
    path('featured/', views.featured_books, name='featured_books'),
    path('out-of-stock/', views.out_of_stock, name='out_of_stock'),
    path('<slug:slug>/', views.book_detail, name='book_detail'),
   

]