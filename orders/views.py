from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File
from django.conf import settings

from wkhtmltopdf.views import PDFTemplateView

from orders.models import OrderItem,Order
from orders.forms import OrderCreateForm

from cart.cart import Cart

# Create your views here.

class OrderPDFView(PDFTemplateView):
    template_name = "order_pdf.html"

    def get_context_data(self, **kwargs):
        #Retrieve order and user information
        order_id = kwargs['pk']
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)

        context = {
            'order':order,
            'order_items':order_items,
        }
        return context
    

def order_create_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.user,request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            print(order)

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity = item['quantity'])
                
            #clear the cart 
            cart.clear()
            #pass the order and the user information to the template
            context = {
                'order':order,
                'user':request.user,
                'order_items':OrderItem.objects.filter(order=order)

            }
            





        return render(request,'order_created.html',context)
    
    else:
        print(request.user)
        form = OrderCreateForm(user=request.user)
      


    return render(request,'order_create.html',{'cart':cart,'form':form})