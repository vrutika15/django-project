from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .forms import ProjectResourceForm as ProjectForm
from .models import ProjectModel
from .forms import ProjectForm, ProjectResourceFormSet


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
    projects = ProjectModel.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


def project_create(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        formset = ProjectResourceFormSet(request.POST)
        if project_form.is_valid() and formset.is_valid():
            project = project_form.save()
            formset.instance = project
            formset.save()
            return redirect('projects:project_list')
    else:
        project_form = ProjectForm()
        formset = ProjectResourceFormSet()

    return render(request, 'projects/project_form.html', {
        'form': project_form,
        'formset': formset,
        'title': 'Create Project'
    })


def project_edit(request, pk):
    project = get_object_or_404(ProjectModel, pk=pk)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        formset = ProjectResourceFormSet(request.POST, instance=project)
        if project_form.is_valid() and formset.is_valid():
            project_form.save()
            formset.save()
            return redirect('projects:project_list')
    else:
        project_form = ProjectForm(instance=project)
        formset = ProjectResourceFormSet(instance=project)

    return render(request, 'projects/project_form.html', {
        'form': project_form,
        'formset': formset,
        'title': 'Edit Project'
    })


def project_delete(request, pk):
    project = get_object_or_404(ProjectModel, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects:project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})


