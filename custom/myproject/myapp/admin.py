# admin.py

from django.contrib import admin
from .models import Employee, Project, Assignment

class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1  # Number of empty forms to display
    verbose_name = "Project Assignment"
    verbose_name_plural = "Project Assignments"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj and not obj.is_active:  # Check if the employee is inactive
            for form in formset.forms:
                form.fields['project'].disabled = True  # Disable project selection
                form.fields['role'].disabled = True      # Disable role selection
                form.fields['hours_per_week'].disabled = True  # Disable hours input
        return formset

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department', 'date_joined', 'is_active')
    inlines = [AssignmentInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.is_active:
            # Remove all assignments for inactive employees
            Assignment.objects.filter(employee=obj).delete()

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_completed')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'project', 'role', 'hours_per_week')
