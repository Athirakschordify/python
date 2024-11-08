# from django.contrib import admin
# from .models import Book

# admin.site.register(Book)


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .models import Book

class BookAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('myapp/custom_admin.css',)
        }

admin.site.register(Book, BookAdmin)

