from django.urls import path
from . import views

app_name = 'author'

urlpatterns = [
    path('', views.author_list_view, name='author_list'),
    path('create/', views.author_create_view, name='author_create'),
    path('edit/<int:author_id>/', views.author_edit_view, name='author_edit'),
    path('delete/<int:author_id>/', views.author_delete_view, name='author_delete'),
    path('<int:author_id>/', views.author_detail_view, name='author_detail'),
]