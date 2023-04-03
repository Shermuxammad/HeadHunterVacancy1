from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('create/', views.menu_create, name='menu_create'),
    path('edit/<int:pk>/', views.menu_edit, name='menu_edit'),
    path('delete/<int:pk>/', views.menu_delete, name='menu_delete'),
    path('menu/', views.MenuView.as_view(), name='menu'),

]
