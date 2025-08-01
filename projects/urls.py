from django.urls import path
from . import views
from .views import dashboard_home

app_name = 'projects'   

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('list/', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
]
