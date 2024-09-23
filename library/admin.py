from django.contrib import admin
from .models import *
from django.utils.html import format_html
from .forms import *
from django.http import FileResponse
from .pdf_generator import generate_invoice_pdf

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

def download_invoice_pdf(modeladmin, request, queryset):
    if queryset.count() == 1:
        invoice = queryset.first()
        pdf_buffer = generate_invoice_pdf(invoice.id)
        response = FileResponse(pdf_buffer, as_attachment=True, filename=f"invoice_{invoice.id}.pdf")
        return response
    else:
        pass
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_generated', 'total_amount', 'is_paid')
    actions = [download_invoice_pdf]
admin.site.register(Invoice, InvoiceAdmin)