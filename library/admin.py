from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book, BookAdmin)

