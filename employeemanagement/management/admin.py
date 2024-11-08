from django.contrib import admin
from django.forms import ModelForm, ValidationError
from .models import Employee, Project, Assignment

class AssignmentInlineForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if self.instance.employee and not self.instance.employee.is_active:
            raise ValidationError("Cannot assign inactive employees to projects.")
        return cleaned_data

class AssignmentInline(admin.TabularInline):
    model = Assignment
    form = AssignmentInlineForm
    extra = 1

    def has_add_permission(self, request, obj):
        if obj and not obj.is_active:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if obj and not obj.is_active:
            return False
        return True

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "department", "is_active", "date_joined")
    list_filter = ("department", "is_active")
    search_fields = ("first_name", "last_name", "department")
    inlines = [AssignmentInline]

    def save_model(self, request, obj, form, change):
        if not obj.is_active:
            Assignment.objects.filter(employee=obj).delete()
        super().save_model(request, obj, form, change)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Project)
