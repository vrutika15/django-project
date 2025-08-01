from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from .models import ResourceModel

def dashboard_home(request):
    years = list(range(2020, 2031))
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    return render(request, 'home.html', {
        'years': years,
        'months': months,
        'current_year': datetime.now().year
    })

