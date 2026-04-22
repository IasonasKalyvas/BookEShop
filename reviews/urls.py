from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path('', views.review_page, name='review_page'),
    path('manage/', views.manage_reviews, name='manage_reviews'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]