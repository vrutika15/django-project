# resources-models
from django.db import models
import calendar
from datetime import date
 
# Create your models here.

MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]

class ResourceModel(models.Model):
    """
    Stores resource (developer/employee) data with logic to auto-calculate
    working days based on a standard month schedule.
    """
 
    resource_name = models.CharField(
        max_length=100,
        blank=False,
        help_text="Enter the full name of the resource"
    )
 
    working_days = models.FloatField(
        null=True,
        blank=True,
        help_text="Leave blank to auto-calculate (Mon–Fri + 1st Saturday)"
    )
 
    present_day = models.FloatField(
        default=0,
        help_text="Days resource was present"
    )
 
    present_hours = models.FloatField(
        default=0,
        help_text="Auto-calculated as present_day × 8 hours if not set"
    )

    year = models.IntegerField(default=date.today().year)
    month = models.IntegerField(choices=MONTH_CHOICES, default=date.today().month)
 
    @staticmethod
    def get_working_days(year=None, month=None):
        """
        Calculate working days for a given year and month (Mon–Fri + 1st Saturday).
        """
        today = date.today()
        year = year or today.year
        month = month or today.month
 
        _, num_days = calendar.monthrange(year, month)
        first_day = calendar.monthrange(year, month)[0]
 
        # Get the date of the 1st Saturday
        first_saturday = (5 - first_day) % 7 + 1
        if first_saturday > num_days:
            first_saturday = None  # Just in case
 
        working_days = 0
        for day in range(1, num_days + 1):
            weekday = (first_day + day - 1) % 7
            if weekday < 5:  # Monday to Friday
                working_days += 1
 
        if first_saturday:
            working_days += 1
 
        return working_days
 
    def save(self, *args, **kwargs):
        # Set working days if not manually entered
        if not self.working_days:
            self.working_days = self.get_working_days()
 
        # Set present hours if not provided
        if self.present_day and not self.present_hours:
            self.present_hours = self.present_day * 8
 
        super().save(*args, **kwargs)
 
    def get_working_days_for_display(self):
        today = date.today()
        wd = self.get_working_days()
        return f"{wd} days ({today.strftime('%B %Y')})"
 
    def __str__(self):
        return self.resource_name
 
    class Meta:
        db_table = 'resource_model'
        ordering = ['resource_name']
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'