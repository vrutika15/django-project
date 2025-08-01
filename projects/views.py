from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Project
from .forms import ProjectForm


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

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


def project_create(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        print("POST data:", request.POST)  # Debugging: Print POST data
        if project_form.is_valid():
            print("Form is valid!")  # Debugging: Form is valid
            project = project_form.save()  # Save the project first
            
            # Get the list of selected resources
            resources = request.POST.getlist('resources')
            print(f"Selected resources: {resources}")  # Debugging: Selected resources

            # Assign resources to the project
            project.resources.set(resources)  # Associate selected resources to the project
            project.save()  # Save the project again after assigning resources

            return redirect('projects:project_list')  # Redirect after success
        else:
            print(f"Form errors: {project_form.errors}")  # Debugging: Print form errors
    else:
        project_form = ProjectForm()

    return render(request, 'projects/project_form.html', {
        'form': project_form,
        'title': 'Create Project'
    })


def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project_form.save()
            return redirect('projects:project_list')
    else:
        project_form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {
        'form': project_form,
        'title': 'Edit Project'
    })


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects:project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})
