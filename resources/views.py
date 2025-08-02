from django.shortcuts import render, redirect, get_object_or_404
from .models import Resource
from projects.models import Project
from .forms import ResourceForm
from django.contrib import messages

def home_page(request):
    return render(request, 'home.html')

def attendance_home(request):
    resources = Resource.objects.all()
    projects = Project.objects.prefetch_related('resources').all()

    # Totals for resource
    total_working_days = sum(r.working_days for r in resources)
    total_present_days = sum(r.present_day for r in resources)
    total_present_hours = sum(r.present_hours for r in resources)
    presence_percentage = (100 * total_present_days)/total_working_days

    # Totals for project
    total_billable_days = sum(p.billable_days for p in projects)
    total_non_billable_days = sum(p.non_billable_days for p in projects)
    total_billable_hours = sum(p.billable_hours for p in projects)
    total_non_billable_hours = sum(p.non_billable_hours for p in projects)

    context = {
        'resources': resources,
        'projects': projects,
        'total_working_days': total_working_days,
        'total_present_days': total_present_days,
        'total_present_hours': total_present_hours,
        'total_billable_days': total_billable_days,
        'total_non_billable_days': total_non_billable_days,
        'total_billable_hours': total_billable_hours,
        'total_non_billable_hours': total_non_billable_hours,
        'presence_percentage' : presence_percentage
    }

    return render(request, 'attendance/attendance_home.html', context)

def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'resources/resource_list.html', {'resources': resources, 'title': 'Resources'})

def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource created successfully.')
            return redirect('resource_list')
    else:
        form = ResourceForm()

    year_range = range(2020, 2031)

    month_choices = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]
    
    return render(request, 'resources/resource_form.html', {
        'form': form,
        'title': 'Add Resource',
        'month_choices': month_choices,
        'year_range': year_range,
    })


def resource_update(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource updated successfully.')
            return redirect('resource_list')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resources/resource_form.html', {'form': form, 'title': 'Edit Resource'})

def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted successfully.')
        return redirect('resource_list')
    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})
