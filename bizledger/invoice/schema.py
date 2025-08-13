
import graphene
from graphene_django.types import DjangoObjectType
from .models import Invoice
from .utils import generate_invoice_pdf
import base64

class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoice
        fields = ("id", "project", "amount", "status", "created_at", "due_date")

class Query(graphene.ObjectType):
    invoices = graphene.List(InvoiceType, status=graphene.String())

    def resolve_invoices(self, info, status=None):
        if status:
            return Invoice.objects.filter(status=status)
        return Invoice.objects.all()

class CreateInvoice(graphene.Mutation):
    invoice = graphene.Field(InvoiceType)

    class Arguments:
        project_id = graphene.ID(required=True)
        amount = graphene.Float(required=True)
        due_date = graphene.Date()

    def mutate(self, info, project_id, amount, due_date=None):
        from core.models import Project
        project = Project.objects.get(id=project_id)
        invoice = Invoice(project=project, amount=amount, status="unpaid", due_date=due_date)
        invoice.save()
        return CreateInvoice(invoice=invoice)

class GenerateInvoicePDF(graphene.Mutation):
    pdf = graphene.String()

    class Arguments:
        invoice_id = graphene.ID(required=True)

    def mutate(self, info, invoice_id):
        pdf = generate_invoice_pdf(invoice_id)
        pdf_base64 = base64.b64encode(pdf).decode('utf-8')
        return GenerateInvoicePDF(pdf=pdf_base64)

class Mutation(graphene.ObjectType):
    create_invoice = CreateInvoice.Field()
    generate_invoice_pdf = GenerateInvoicePDF.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
