from django.db import models
from core.models import Category


class Expense(models.Model):
    EXPENSE_TYPES = [
        ('employer', 'Employer'),
        ('supplier', 'Supplier'),
        ('subscription', 'Subscription'),
        ('one_time', 'One-Time Payment'),
        ('monthly', 'Monthly Payment'),
        ('yearly', 'Yearly Payment'),
    ]

    vendor = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'type': 'expense'})
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)  # Optional for details

    def __str__(self):
        return f"{self.vendor} - {self.amount} ({self.expense_type})"