from django.contrib import admin
from .models import *
from django.utils.html import format_html
from .forms import *

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price')
admin.site.register(Book, BookAdmin)

class DebtAdmin(admin.ModelAdmin):
    pass    
admin.site.register(Debt, DebtAdmin)
class BorrowingAdmin(admin.ModelAdmin):
    pass    
admin.site.register(Borrowing, BorrowingAdmin)

class ReturningAdmin(admin.ModelAdmin):
    pass    
admin.site.register(Returning, ReturningAdmin)