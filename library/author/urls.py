from django.urls import path
from . import views

app_name = 'author'

urlpatterns = [
    path('', views.author_list_view, name='author_list'),
    path('create/', views.author_create_view, name='author_create'),
    path('<int:author_id>/edit/', views.author_edit_view, name='author_edit'),
    path('<int:author_id>/delete', views.author_delete_view, name='author_delete'),
    path('<int:author_id>/', views.author_detail_view, name='author_detail'),
]