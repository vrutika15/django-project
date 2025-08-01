# models - projects
from django.db import models
from resources.models import ResourceModel
from django.core.validators import MinValueValidator
from django.urls import reverse
 
# Create your models here.
 
class ProjectModel(models.Model):
    """
    Represents a project and its overall time tracking.
    """
 
    PROJECT_TYPE_CHOICES = [
        ('REGULAR', 'Regular Project'),
        ('FIXED_COST', 'Fixed Cost Project'),
    ]
 
    project_name = models.CharField(max_length=100)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, default='REGULAR')
 
    billable_days = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total billable days for the project"
    )
 
    non_billable_days = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total non-billable days for the project"
    )
 
    billable_hours = models.FloatField(
        default=0,
        editable=False,
        help_text="Auto-calculated (billable_days × 8)"
    )
 
    non_billable_hours = models.FloatField(
        default=0,
        editable=False,
        help_text="Auto-calculated (non_billable_days × 8)"
    )
 
    resources = models.ManyToManyField(
        ResourceModel,
        through='ProjectResource',
        through_fields=('project', 'resource'),
        related_name='projects'
    )
 
    is_active = models.BooleanField(default=True)  # For soft-deletion
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def save(self, *args, **kwargs):
        self.billable_hours = self.billable_days * 8
        self.non_billable_hours = self.non_billable_days * 8
        super().save(*args, **kwargs)
 
    def __str__(self):
        return self.project_name
 
    def get_absolute_url(self):
        return reverse('projects:project_detail', args=[str(self.id)])
 
    @property
    def resource_count(self):
        return self.resources.count()
 
    @property
    def total_hours(self):
        return self.billable_hours + self.non_billable_hours
 
    @property
    def utilization_percentage(self):
        if self.resource_count == 0:
            return 0
        standard_hours = 8 * 22  # Default monthly working hours
        utilization = (self.total_hours / standard_hours) * 100
        return min(utilization, 100)
 
    def get_resource_utilization(self, resource):
        try:
            allocation = self.projectresource_set.get(resource=resource)
            return {
                'present_days': allocation.present_day,
                'billable_days': allocation.billable_days,
                'billable_hours': allocation.billable_hours,
                'non_billable_days': allocation.non_billable_days,
                'non_billable_hours': allocation.non_billable_hours,
                'total_hours': allocation.billable_hours + allocation.non_billable_hours
            }
        except ProjectResource.DoesNotExist:
            return None
 
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
 
class ProjectResource(models.Model):
    """
    Tracks each resource's time allocation for a specific project.
    """
 
    project = models.ForeignKey(
        ProjectModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='project_resources'
    )
 
    resource = models.ForeignKey(
        ResourceModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='project_allocations'
    )
 
    present_day = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Days the resource was present for this project"
    )
 
    billable_days = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of billable days"
    )
 
    billable_hours = models.FloatField(
        default=0,
        editable=False,
        help_text="Auto-calculated (billable_days × 8)"
    )
 
    non_billable_days = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of non-billable days"
    )
 
    non_billable_hours = models.FloatField(
        default=0,
        editable=False,
        help_text="Auto-calculated (non_billable_days × 8)"
    )
 
    is_active = models.BooleanField(default=True)  # Optional soft-delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def save(self, *args, **kwargs):
        self.billable_hours = self.billable_days * 8
        self.non_billable_hours = self.non_billable_days * 8
        super().save(*args, **kwargs)
 
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'resource'], name='unique_project_resource')
        ]
        ordering = ['-created_at']
 
    def __str__(self):
        return f"{self.resource} - {self.project}"
 
 