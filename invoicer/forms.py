# forms.py
from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['manual_user_id', 'invoice_number', 'date', 'description', 'amount', 'business', 'customer', 'agent']
