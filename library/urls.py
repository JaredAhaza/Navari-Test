from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books', views.books, name='books'),
    path('search/', views.search_books, name='search_books')
]