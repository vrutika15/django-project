from django import forms
from .models import Resource as ResourceModel
from datetime import date

class ResourceForm(forms.ModelForm):
    class Meta:
        model = ResourceModel
        fields = ['resource_name', 'working_days', 'present_day', 'present_hours', 'year', 'month']
        widgets = {
            'resource_name': forms.TextInput(attrs={'class': 'form-control'}),
            'working_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'placeholder': 'Leave blank for auto-calculation'
            }),
            'present_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'present_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
        }
        labels = {
            'resource_name': 'Resource Name',
            'present_day': 'Days Present',
            'present_hours': 'Hours Present',
            'year': 'Year',
            'month': 'Month',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically create choices for the year (2020 to 2031)
        year_choices = [(year, year) for year in range(2020, 2032)]
        self.fields['year'] = forms.ChoiceField(
            choices=year_choices, 
            widget=forms.Select(attrs={'class': 'form-select'}), 
            initial=date.today().year
        )

        # Dynamically create choices for the months (1 to 12)
        month_choices = [(i, month) for i, month in enumerate([
            'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December'
        ], 1)]
        self.fields['month'] = forms.ChoiceField(
            choices=month_choices, 
            widget=forms.Select(attrs={'class': 'form-select'}),
            initial=date.today().month
        )
        
        # Add help text for working days
        self.fields['working_days'].required = False
        if self.instance and self.instance.pk:
            self.fields['working_days'].help_text = f"Auto-calculated value: {self.instance.get_working_days_for_display()}"
        else:
            current_date = date.today()
            default_working_days = ResourceModel.get_working_days(current_date.year, current_date.month)
            self.fields['working_days'].help_text = f"Auto-calculated if left blank: {default_working_days} days (current month)"

    def clean(self):
        """
        Custom clean method to calculate present_hours dynamically if present_day is provided.
        """
        cleaned_data = super().clean()
        
        # Get present_day value
        present_day = cleaned_data.get('present_day')
        
        # Calculate present_hours if present_day is provided
        if present_day is not None:
            cleaned_data['present_hours'] = present_day * 8
        
        return cleaned_data