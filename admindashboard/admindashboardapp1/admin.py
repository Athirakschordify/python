from django.contrib import admin

# Register your models here.
from . import models

class MovieAdmin(admin.ModelAdmin):
# ORDERING FIELDS
    fields=['release_year','length','title']
# SEARCHING FIELDS
    search_fields=['title','length','release_year']
# ADDING FILTER
    list_filter=['title','length','release_year']
# ADDING FIELDS
    list_display=['title','length','release_year']
# EDITABLE LIST
    list_editable=['length']    


     



admin.site.register(models.Movie,MovieAdmin)
admin.site.register(models.Customer)