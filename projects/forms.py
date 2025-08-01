from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import ProjectModel, ProjectResource
from resources.models import ResourceModel

# ✅ Project Form (main)
class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['project_name', 'project_type', 'billable_days', 'non_billable_days', 'resources']
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name',
                'required': True
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'billable_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.5',
                'value': '0',
                'required': False
            }),
            'non_billable_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.5',
                'value': '0',
                'required': False
            }),
        }
        labels = {
            'project_name': 'Project Name',
            'project_type': 'Project Type',
            'billable_days': 'Billable Days',
            'non_billable_days': 'Non-Billable Days',
            'resources': 'Select Resources',
        }

    def clean(self):
        cleaned_data = super().clean()
        billable_days = cleaned_data.get('billable_days', 0)
        non_billable_days = cleaned_data.get('non_billable_days', 0)

        if billable_days < 0 or non_billable_days < 0:
            raise forms.ValidationError("Days cannot be negative")

        return cleaned_data

# ✅ Inline Resource Form
class ProjectResourceForm(forms.ModelForm):
    class Meta:
        model = ProjectResource
        fields = ['resource', 'present_day', 'billable_days', 'non_billable_days']
        widgets = {
            'resource': forms.Select(attrs={
                'class': 'form-select resource-select',
                'required': 'required'
            }),
            'present_day': forms.NumberInput(attrs={
                'class': 'form-control present-days',
                'step': '0.5',
                'min': '0',
                'required': 'required'
            }),
            'billable_days': forms.NumberInput(attrs={
                'class': 'form-control billable-days',
                'step': '0.5',
                'min': '0',
                'required': 'required'
            }),
            'non_billable_days': forms.NumberInput(attrs={
                'class': 'form-control non-billable-days',
                'step': '0.5',
                'min': '0',
                'required': 'required'
            }),
        }
        labels = {
            'resource': 'Resource',
            'present_day': 'Present Days',
            'billable_days': 'Billable Days',
            'non_billable_days': 'Non-Billable Days',
        }

    def clean(self):
        cleaned_data = super().clean()
        present_day = cleaned_data.get('present_day', 0)
        billable_days = cleaned_data.get('billable_days', 0)
        non_billable_days = cleaned_data.get('non_billable_days', 0)

        if billable_days + non_billable_days > present_day:
            raise forms.ValidationError("Billable + Non-billable days cannot exceed present days.")

        return cleaned_data


# ✅ Inline formset
class ProjectResourceFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not hasattr(form, 'cleaned_data') or not form.cleaned_data:
                continue
            present_day = form.cleaned_data.get('present_day', 0)
            if present_day and present_day < 0:
                form.add_error('present_day', 'Present days cannot be negative')


ProjectResourceFormSet = inlineformset_factory(
    ProjectModel,
    ProjectResource,
    form=ProjectResourceForm,
    formset=ProjectResourceFormSet,
    extra=0,
    can_delete=False,
    min_num=0,
    validate_min=True
)
