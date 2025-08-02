from django.urls import path
from . import views
from .views import dashboard_home

app_name = 'projects'   

urlpatterns = [
    path('projects/dashboardhome', views.dashboard_home, name='dashboard_home'),
    # path('projects/list/', views.project_list, name='project_list'),
    path('', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    # path('attendance/', views.sum_projects, name='attendance_home')
]
