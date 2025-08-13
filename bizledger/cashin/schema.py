import graphene
from graphene_django.types import DjangoObjectType
from .models import Payment
from core.models import Category, Project

class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = ("id", "project", "amount", "category", "date")

class Query(graphene.ObjectType):
    payments = graphene.List(PaymentType)
    total_income = graphene.Float(year=graphene.Int(), month=graphene.Int())

    def resolve_payments(self, info):
        return Payment.objects.all()

    def resolve_total_income(self, info, year=None, month=None):
        from datetime import date
        year = year or date.today().year
        month = month or date.today().month
        payments = Payment.objects.filter(date__year=year, date__month=month)
        return float(sum(payment.amount for payment in payments) or 0)

class RecordPayment(graphene.Mutation):
    payment = graphene.Field(PaymentType)

    class Arguments:
        project_id = graphene.ID()
        amount = graphene.Float(required=True)
        category_id = graphene.ID(required=True)

    def mutate(self, info, amount, category_id, project_id=None):
        category = Category.objects.get(id=category_id, type='income')
        payment = Payment(amount=amount, category=category)
        if project_id:
            project = Project.objects.get(id=project_id)
            payment.project = project
            project.paid += amount
            project.save()
        payment.save()
        return RecordPayment(payment=payment)

class Mutation(graphene.ObjectType):
    record_payment = RecordPayment.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
