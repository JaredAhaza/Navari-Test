from django.contrib import admin
from .models import *
from django.utils.html import format_html
from .forms import *

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book, BookAdmin)


class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('book', 'customer', 'issue_date', 'return_date', 'fee', 'is_returned', 'is_late', 'is_damaged')
    list_filter = ('is_returned', 'is_late', 'is_damaged')
    search_fields =('book__title', 'customer__username')
    actions = ['issue_book', 'return_book']

    def issue_book(self, request, queryset):
        for borrowing in queryset:
            if borrowing.is_returned:
                self.message_user(request, "Book is already returned")
                return
            borrowing.issue_date = datetime.datetime.now()
            borrowing.save()
        self.message_user(request, "Book issued successfully")
    issue_book.short_description = "Issue selected book"


    def return_book(self, request, queryset):
        for borrowing in queryset:
            if not borrowing.is_returned:
                self.message_user(request, "Book is not issued")
                return
            borrowing.return_date = datetime.date.today()
            borrowing.is_returned = True
            borrowing.save()
        self.media(request, "Book returned successfully")
    return_book.short_description = "Return selected book"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "customer":
            kwargs["queryset"] = Customer.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['fee'].initial = 0
        return form
    
admin.site.register(Borrowing, BorrowingAdmin)