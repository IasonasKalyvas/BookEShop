from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path('', views.review_page, name='review_page'),
]