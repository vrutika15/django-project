from django.urls import path
from .views import dashboard_home

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),
]
