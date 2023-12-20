from django import forms
from django.forms import widgets

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,21)]


class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    quantity = forms.IntegerField()
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
    