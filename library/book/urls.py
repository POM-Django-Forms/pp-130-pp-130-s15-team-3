from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('user/<int:user_id>/', views.user_books, name='user_books'),
]
