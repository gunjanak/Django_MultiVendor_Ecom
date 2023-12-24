from django.shortcuts import render,redirect,get_list_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from vendors.models import Product

from cart.cart import Cart
from cart.forms import CartAddProductForm


# Create your views here.
@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_list_or_404(Product,id=product_id)
    product = product[0]
    form = CartAddProductForm(request.POST)
    form.product = product #set the product attribute 

    print("*******************")
    print(product)
   

    if form.is_valid():
        cd = form.cleaned_data
        print(product.items_in_store)
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        return redirect('cart:cart_detail')
    return render(request,'vendors/product_detail.html',{'product':product,'cart_form':form})
        
    
@require_POST 
def cart_remove(request,product_id):
    print("**************************")
    print(f"Removing {product_id}")
    cart = Cart(request)
    product =get_list_or_404(Product,id=product_id)
    print(product[0])
    cart.remove(product[0])
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)

    for item in cart:
        item['form'] = CartAddProductForm(initial={
            'quantity':item['quantity'],
            'override':True
        })
        # print(item['form'])
    return render(request,'cart/detail.html',{'cart':cart})