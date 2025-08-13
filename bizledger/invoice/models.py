from django.db import models
from core.models import Project

class Invoice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')])
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.project.name}"
