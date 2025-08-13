
import graphene
from graphene_django.types import DjangoObjectType
from core.models import Client, Project, Category
from cashin.schema import Query as CashInQuery, Mutation as CashInMutation
from cashout.schema import Query as CashOutQuery, Mutation as CashOutMutation
from invoice.schema import Query as InvoiceQuery, Mutation as InvoiceMutation
from datetime import date

class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = ("id", "name", "email", "phone", "notes", "projects")

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ("id", "client", "name", "description", "start_date", "end_date", "budget", "paid", "invoices")

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "type")

class CashFlowType(graphene.ObjectType):
    total_income = graphene.Float()
    total_expenses = graphene.Float()
    net_cash_flow = graphene.Float()

class Query(CashInQuery, CashOutQuery, InvoiceQuery, graphene.ObjectType):
    clients = graphene.List(ClientType)
    projects = graphene.List(ProjectType)
    categories = graphene.List(CategoryType)
    cash_flow = graphene.Field(CashFlowType, year=graphene.Int(), month=graphene.Int())

    def resolve_clients(self, info):
        return Client.objects.all()

    def resolve_projects(self, info):
        return Project.objects.all()

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_cash_flow(self, info, year=None, month=None):
        from cashin.models import Payment
        from cashout.models import Expense
        year = year or date.today().year
        month = month or date.today().month
        payments = Payment.objects.filter(date__year=year, date__month=month)
        expenses = Expense.objects.filter(date__year=year, date__month=month)
        total_income = sum(payment.amount for payment in payments) or 0
        total_expenses = sum(expense.amount for expense in expenses) or 0
        return CashFlowType(
            total_income=float(total_income),
            total_expenses=float(total_expenses),
            net_cash_flow=float(total_income - total_expenses)
        )

class Mutation(CashInMutation, CashOutMutation, InvoiceMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
