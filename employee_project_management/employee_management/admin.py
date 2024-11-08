from django.contrib import admin
from .models import Employee, Project, Assignment



class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'department', 'date_joined', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('first_name', 'last_name', 'department')
    list_editable=['department']

   

# Register models in admin
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Project)
admin.site.register(Assignment)
