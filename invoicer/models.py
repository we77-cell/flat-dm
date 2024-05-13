# models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manual_user_id = models.IntegerField()
    invoice_number = models.CharField(max_length=10)
    date_created = models.DateTimeField(default=timezone.now)
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    business = models.CharField(max_length=100, default="Business Name")  # New field 'business'
    customer = models.CharField(max_length=100, default='Customer Name')  # New field 'customer'
    agent = models.CharField(max_length=100, default='Agent Name')  # New field 'agent'
    

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.user.username}"

class DailyTotal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_amount_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_calculated_day = models.PositiveIntegerField(default=0)