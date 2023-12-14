# forms.py

from django import forms
from .models import Product, Service

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item_name', 'description', 'image', 'category', 'items_in_store', 'price']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['item_name', 'description', 'image', 'category', 'is_active', 'pricing_type', 'hourly_rate', 'daily_rate', 'per_job_rate']
