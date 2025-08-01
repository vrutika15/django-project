from django import forms
from .models import ResourceModel
 
class ResourceForm(forms.ModelForm):
    class Meta:
        model = ResourceModel
        fields = ['resource_name', 'working_days', 'present_day', 'year', 'month']
        widgets = {
            'resource_name': forms.TextInput(attrs={'class': 'form-control'}),
            'working_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'placeholder': 'Leave blank for auto-calculation'
            }),
            'present_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            # 'present_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'year': forms.HiddenInput(),
            'month': forms.HiddenInput(),
        }
        labels = {
            'resource_name': 'Resource Name',
            'present_day': 'Days Present',
            # 'present_hours': 'Hours Present',
        }
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text for working days
        self.fields['working_days'].required = False
       
        # Show calculated working days info for existing instances
        if self.instance and self.instance.pk:
            self.fields['working_days'].help_text = f"Auto-calculated value: {self.instance.get_working_days_for_display()}"
        else:
            self.fields['working_days'].help_text = f"Auto-calculated if left blank: {ResourceModel().get_working_days_for_display()}"
 
 