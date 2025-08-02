from django import forms
from .models import Project
from resources.models import Resource


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name',
            'project_type',
            'year',
            'month',
            'resources',
            'present_day',
            'billable_days',
            'non_billable_days'
        ]
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name',
                'required': True
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2020,
                'max': 2035
            }),
            'month': forms.Select(attrs={
                'class': 'form-select'
            }),
            'resources': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
            'present_day': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.5
            }),
            'billable_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.5
            }),
            'non_billable_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.5
            }),
        }
        labels = {
            'project_name': 'Project Name',
            'project_type': 'Project Type',
            'year': 'Year',
            'month': 'Month',
            'resources': 'Assigned Resources',
            'present_day': 'Present Days',
            'billable_days': 'Billable Days',
            'non_billable_days': 'Non-Billable Days',
        }

    def clean(self):
        cleaned_data = super().clean()
        billable = cleaned_data.get('billable_days') or 0
        non_billable = cleaned_data.get('non_billable_days') or 0
        present = cleaned_data.get('present_day') or 0

        #ensure no negative values for days
        if billable < 0 or non_billable < 0 or present < 0:
            raise forms.ValidationError("Days cannot be negative.")

        #sum of billable + non-billable days does not exceed present days
        if billable > present:
            raise forms.ValidationError("Billable days cannot be more than present days.")

        return cleaned_data
