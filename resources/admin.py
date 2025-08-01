# resources - admin.py
from django.contrib import admin
from .models import ResourceModel
 
# Register your models here.
 
@admin.register(ResourceModel)
class ResourceModelAdmin(admin.ModelAdmin):
    list_display = (
        'resource_name',
        'working_days',
        'present_day',
        'present_hours',
    )
    search_fields = ('resource_name',)
    list_filter = ('working_days',)
 
 