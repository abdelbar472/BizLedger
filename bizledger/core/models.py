from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} ({self.client.name})"

class Category(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Client Payments", "Software"
    type = models.CharField(max_length=20, choices=[('income', 'Income'), ('expense', 'Expense')])

    def __str__(self):
        return self.name