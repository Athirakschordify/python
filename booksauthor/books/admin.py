# from django.contrib import admin
# from . import models

# # Register your models here.
# admin.site.register(models.Author)
# admin.site.register(models.Book)

# admin.py
from django.contrib import admin
from . import models

class BookAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('library/admin_custom.css',)
        }

class AuthorAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('library/admin_custom.css',)
        }        

# Register your models with the custom BookAdmin
admin.site.register(models.Author,AuthorAdmin)
admin.site.register(models.Book, BookAdmin)
