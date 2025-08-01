# projects-admin
from django.contrib import admin
from .models import ProjectModel, ProjectResource
 
# Register your models here.
 
class ProjectResourceInline(admin.TabularInline):
    """
    Allows managing ProjectResource entries directly from the ProjectModel admin page.
    """
    model = ProjectResource
    extra = 1
    autocomplete_fields = ['resource']
    readonly_fields = ('billable_hours', 'non_billable_hours')
    verbose_name = "Project Allocation"
    verbose_name_plural = "Project Allocations"
 
 
@admin.register(ProjectModel)
class ProjectModelAdmin(admin.ModelAdmin):
    list_display = (
        'project_name',
        'project_type',
        'billable_days',
        'non_billable_days',
        'billable_hours',
        'non_billable_hours',
        'resource_count',
        'utilization_percentage',
        'is_active',
        'updated_at',
    )
    list_filter = ('project_type', 'is_active')
    search_fields = ('project_name',)
    inlines = [ProjectResourceInline]
    readonly_fields = ('billable_hours', 'non_billable_hours', 'created_at', 'updated_at')
 
 
@admin.register(ProjectResource)
class ProjectResourceAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'resource',
        'present_day',
        'billable_days',
        'billable_hours',
        'non_billable_days',
        'non_billable_hours',
        'created_at',
    )
    search_fields = (
        'project__project_name',
        'resource__resource_name',
    )
    list_filter = ('project', 'resource')
    readonly_fields = ('billable_hours', 'non_billable_hours', 'created_at', 'updated_at')
 
 