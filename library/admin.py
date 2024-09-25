from django.contrib import admin
from .models import *
from django.utils.html import format_html
from .forms import *
from django.http import FileResponse
from .pdf_generator import generate_invoice_pdf
import pdfkit

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'is_available', 'borrowed_by')
    search_fields = ('title', 'author')
    list_filter = ('author', 'category', 'is_available', 'borrowed_by')
admin.site.register(Book, BookAdmin)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_debt')
    search_fields = ('customer', 'total_debt')
    list_filter = ('total_debt', 'customer')    
admin.site.register(Debt, DebtAdmin)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('book', 'customer', 'issue_date', 'book_price')
    search_fields = ('book', 'customer')
    list_filter = ('issue_date', 'customer')
admin.site.register(Borrowing, BorrowingAdmin)
class ReturningAdmin(admin.ModelAdmin):
    list_display = ('borrowing', 'is_returned', 'is_late', 'is_damaged', 'fine')
    search_fields = ('borrowing', 'is_returned', 'is_late', 'is_damaged')
    list_filter = ('is_returned', 'is_late', 'is_damaged')
admin.site.register(Returning, ReturningAdmin)

def download_invoice_pdf(modeladmin, request, queryset):
    if queryset.count() == 1:
        invoice = queryset.first()
        pdf_buffer = generate_invoice_pdf(invoice.id)
        response = FileResponse(pdf_buffer, as_attachment=True, filename=f"invoice_{invoice.id}.pdf")
        return response
    else:
        pass

def mark_as_paid(modeladmin, request, queryset):
    for invoice in queryset:
        if not invoice.is_paid:
            invoice.is_paid = True
            invoice.save()
mark_as_paid.short_description = "Mark selected invoices as paid"
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_generated', 'total_amount', 'is_paid')
    search_fields = ('customer', 'date_generated')
    list_filter = ('date_generated', 'is_paid')
    actions = [mark_as_paid,download_invoice_pdf]
admin.site.register(Invoice, InvoiceAdmin)