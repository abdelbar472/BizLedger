from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from .models import Invoice

def generate_invoice_pdf(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Invoice - FreelanceFlow", styles['Title']))
    elements.append(Paragraph("Your Business Name", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"To: {invoice.project.client.name}", styles['Heading2']))
    elements.append(Paragraph(f"Email: {invoice.project.client.email or 'N/A'}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Invoice #{invoice.id} - {invoice.project.name}", styles['Heading3']))
    elements.append(Paragraph(f"Date: {invoice.created_at.strftime('%Y-%m-%d')}", styles['Normal']))
    elements.append(Paragraph(f"Due Date: {invoice.due_date or 'N/A'}", styles['Normal']))
    elements.append(Paragraph(f"Status: {invoice.status.capitalize()}", styles['Normal']))
    elements.append(Spacer(1, 12))

    data = [['Description', 'Amount'],
            [f"Project: {invoice.project.name}", f"${invoice.amount}"]]
    table = Table(data, colWidths=[400, 100])
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    elements.append(table)

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total: ${invoice.amount}", styles['Heading2']))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("Thank you for your business!", styles['Normal']))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
