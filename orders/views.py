from django.shortcuts import render

from orders.models import OrderItem
from orders.forms import OrderCreateForm

from cart.cart import Cart

# Create your views here.
def order_create_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity = item['quantity'])
                
            #clear the cart 
            cart.clear()




        return render(request,'order_created.html',{"order":order})
    
    else:
        form = OrderCreateForm()


    return render(request,'order_create.html',{'cart':cart,'form':form})