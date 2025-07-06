# Transaction model
from django.db import models
from core.models import User, Statement


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, related_name="transactions")
    
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100)
    is_credit = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.category}"
