
from django.db import models
from core.models import Category, Project

class Payment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'type': 'income'})
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount}"
