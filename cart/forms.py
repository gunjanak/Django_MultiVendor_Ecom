from typing import Any
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField()
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)

  
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product = self.product

        if quantity > product.items_in_store:
            raise ValidationError(f"Only {product.items_in_store} items available")
        return quantity