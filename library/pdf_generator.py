from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import *

def generate_invoice_pdf(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    customer = invoice.customer
    borrowings = Borrowing.objects.filter(customer=customer)


    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # PDF Header
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, 800, f"Invoice for {customer.user.username}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Invoice Date: {invoice.date_generated.strftime('%Y-%m-%d')}")
    p.drawString(100, 760, f"Total amount: {invoice.total_amount} Shillings")

    # line separator
    p.line(100, 740, 500, 740)
    # PDF Table
    y_position = 730
    for borrowing in borrowings:
        if hasattr(borrowing, 'returning'):
            fine = borrowing.returning.fine
            total_fee = borrowing.returning.calculate_total_fee()
        else:
            fine = 0
            total_fee = borrowing.book_price

        p.drawString(100, y_position, f"Book: ({borrowing.book.title})")
        p.drawString(300, y_position, f"Price: {borrowing.book_price} Shillings")
        p.drawString(100, y_position - 20, f"Fine: {fine} Shillings")
        p.drawString(300, y_position - 20, f"Total Fee: {total_fee} Shillings")

        y_position -= 40

    p.drawString(100, y_position - 20, f"Total_due: {total_fee} Shillings")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer