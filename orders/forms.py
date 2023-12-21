from django import forms
from orders.models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','address','postal_code','city']
        
    def __init__(self,user=None,*args,**kwargs):
        super(OrderCreateForm,self).__init__(*args,**kwargs)
        if user and user.is_authenticated:
       
            print("**************")
            print(user)
            profile = user.profile
            self.fields['first_name'].initial = profile.first_name
            self.fields['last_name'].initial = profile.last_name
            self.fields['email'].initial = profile.email
            self.fields['address'].initial = profile.address
            self.fields['postal_code'].initial = profile.postal_code
            self.fields['city'].initial = profile.city

