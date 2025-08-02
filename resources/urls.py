from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/add/', views.resource_create, name='resource_create'),
    path('resources/edit/<int:pk>/', views.resource_update, name='resource_update'),
    path('resources/delete/<int:pk>/', views.resource_delete, name='resource_delete'),
    path('attendance/', views.attendance_home, name='attendance_home'),
]