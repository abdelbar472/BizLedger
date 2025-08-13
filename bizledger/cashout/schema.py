import graphene
from graphene_django.types import DjangoObjectType
from .models import Expense
from core.models import Category
from datetime import date

class ExpenseType(DjangoObjectType):
    class Meta:
        model = Expense
        fields = ("id", "vendor", "amount", "category", "expense_type", "date", "description")

class Query(graphene.ObjectType):
    expenses = graphene.List(ExpenseType, expense_type=graphene.String())
    total_expenses = graphene.Float(year=graphene.Int(), month=graphene.Int(), expense_type=graphene.String())

    def resolve_expenses(self, info, expense_type=None):
        if expense_type:
            return Expense.objects.filter(expense_type=expense_type)
        return Expense.objects.all()

    def resolve_total_expenses(self, info, year=None, month=None, expense_type=None):
        year = year or date.today().year
        month = month or date.today().month
        expenses = Expense.objects.filter(date__year=year, date__month=month)
        if expense_type:
            expenses = expenses.filter(expense_type=expense_type)
        return float(sum(expense.amount for expense in expenses) or 0)

class RecordExpense(graphene.Mutation):
    expense = graphene.Field(ExpenseType)

    class Arguments:
        vendor = graphene.String(required=True)
        amount = graphene.Float(required=True)
        category_id = graphene.ID(required=True)
        expense_type = graphene.String(required=True)
        date = graphene.Date()
        description = graphene.String()

    def mutate(self, info, vendor, amount, category_id, expense_type, date=None, description=None):
        if expense_type not in dict(Expense.EXPENSE_TYPES).keys():
            raise ValueError("Invalid expense type")
        category = Category.objects.get(id=category_id, type='expense')
        expense = Expense(
            vendor=vendor,
            amount=amount,
            category=category,
            expense_type=expense_type,
            date=date or date.today(),
            description=description
        )
        expense.save()
        return RecordExpense(expense=expense)

class Mutation(graphene.ObjectType):
    record_expense = RecordExpense.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)