from django.shortcuts import render, redirect, get_object_or_404
from .models import ResourceModel
from .forms import ResourceForm
from django.contrib import messages



def resource_list(request):
    resources = ResourceModel.objects.all()
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
    return render(request, 'resources/resource_form.html', {'form': form, 'title': 'Add Resource'})

def resource_update(request, pk):
    resource = get_object_or_404(ResourceModel, pk=pk)
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
    resource = get_object_or_404(ResourceModel, pk=pk)
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted successfully.')
        return redirect('resource_list')
    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})





# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import ResourceModel
# from django.http import HttpResponse
# from django.template.loader import render_to_string

# def resources_view(request):
#     if request.method == "POST":
#         try:
#             count = int(request.POST.get("resource_count", 1))
#         except ValueError:
#             messages.error(request, "Invalid resource count.")
#             return redirect("resources")

#         errors = False

#         for i in range(count):
#             name = request.POST.get(f"resource_name_{i}")
#             working_days = request.POST.get(f"working_days_{i}")
#             present_day = request.POST.get(f"present_day_{i}")

#             if not all([name, working_days, present_day]):
#                 messages.error(request, f"All fields are required for Resource {i + 1}")
#                 errors = True
#                 continue

#             try:
#                 working_days = float(working_days)
#                 present_day = float(present_day)
#                 present_hours = present_day * 8  

#                 ResourceModel.objects.create(
#                     resource_name=name,
#                     working_days=working_days,
#                     present_day=present_day,
#                     present_hours=present_hours
#                 )
#             except ValueError:
#                 messages.error(request, f"Invalid numeric input for Resource {i + 1}")
#                 errors = True

#         if not errors:
#             messages.success(request, "Resources added successfully.")
#             return redirect("dashboard_home")

#     context = {}

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         html = render_to_string("resources/resource_form_partial.html", context, request=request)
#         return HttpResponse(html)

#     return render(request, "resources/resources_form.html")
