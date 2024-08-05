from django.db import models
from django.contrib.auth.models import User

class ExchangeRate(models.Model):
    currency_name = models.CharField(max_length=10)
    rate = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency_name}: {self.rate}"

class Order(models.Model):
    currency_name = models.CharField(max_length=10)
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} {self.currency_name} by {self.user.username}"

class AggregatedOrder(models.Model):
    currency_name = models.CharField(max_length=10)
    total_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    orders = models.ManyToManyField(Order, related_name='aggregated_orders')

    def __str__(self):
        return f"Aggregated {self.total_amount} {self.currency_name}"

class ABANAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

class ConsolidatedOrder(models.Model):
    currency_name = models.CharField(max_length=10)
    total_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
