from typing import Any
import pandas as pd

from django import http
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView
from django.http import Http404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view

from cart.forms import CartAddProductForm
from orders.models import Order,OrderItem
from vendors.dataProcess import data_process







from vendors.models import Product,Service
from vendors.forms import ProductForm, ServiceForm
from vendors.serializers import ProductsSerializer,ServiceSerializer

# Create your views here.

class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = "vendors/create_product.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.vendor = self.request.user

        if 'save_and_add_new' in self.request.POST:
            #save and add new logic here
            self.success_url = reverse_lazy("create_product")
        elif 'save' in self.request.POST:
            #Save logic here
            self.success_url = reverse_lazy("home")

        return super().form_valid(form)

class ServiceCreateView(LoginRequiredMixin,CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "vendors/create_service.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        return super().form_valid(form)




class ProductServiceListView(ListView):
    model = Product
    # template_name = "product_service_list.html"
    template_name = "vendors/p_and_s.html"
    context_object_name = "product_service_list"

    def get_queryset(self):
        return Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_list'] = Service.objects.all()
        return context
    

class ProductDetailView(DetailView):
    model = Product
    template_name = "vendors/product_detail.html"
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_form'] = CartAddProductForm()
        return context
    
    
class ServiceDetailView(DetailView):
    model = Service
    template_name = "vendors/service_detail.html"
    context_object_name = "service"


class VendorRequiredMixin(LoginRequiredMixin):
    """
    Mixin to ensure that the logged-in user is the vendor
    """

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().vendor != self.request.user:
            raise Http404("You do not have permission to edit this")
        return super().dispatch(request,*args,**kwargs)
    

class ProductUpdateView(VendorRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "vendors/edit_product.html"
    success_url = reverse_lazy("home")

class ServiceUpdateView(VendorRequiredMixin,UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "vendors/edit_service.html"
    success_url = reverse_lazy('home')


class ProductDeleteView(VendorRequiredMixin,DeleteView):
    model = Product
    context_object_name = "product"
    template_name = "vendors/delete_product.html"
    success_url = reverse_lazy("home")

class ServiceDeleteView(VendorRequiredMixin,DeleteView):
    model = Service
    context_object_name = "service"
    template_name = "vendors/delete_service.html"
    success_url = reverse_lazy("home")

class UserProductServiceListView(LoginRequiredMixin,ListView):
    template_name = "vendors/user_product_service_list.html"
    context_object_name = "user_product_service_list"

    def get_queryset(self):
        user = self.request.user
        product_queryset = Product.objects.filter(vendor=user)
        service_queryset = Service.objects.filter(vendor = user)

        #All the orderItem related to the vendor
        orderItem_queryset = OrderItem.objects.filter(product__vendor=user)
        data = []
        for idx,order_item in enumerate(orderItem_queryset,start=1):
            data.append({
                'sn':idx,
                "Order id":order_item.order.id,
                "Date":order_item.order.created,
                "Product":order_item.product.item_name,
                "Category":order_item.product.category.name,
                "Items Sold":order_item.quantity,
                "Price":order_item.price,
            })
        df = pd.DataFrame(data)
        df['Date'] = df['Date'].dt.date
        # print(df)
        chart_data_json,line_chart_data_json,line_chart_data_price_json, pie_chart_data_price_json,product_list,chart_data_product = data_process(df)
        
        all_my_products = []
        for product in product_queryset:
            product_sell = {}
           
            product_sold = 0
            pending_orders = 0
            for order in orderItem_queryset:
                if(order.product == product):
                    if(order.order.paid):
                        product_sold += order.quantity
                    else:
                        pending_orders += order.quantity
            product_sell["product"] = product
            product_sell["total_sold"] = product_sold
            product_sell["PendingOrders"] = pending_orders
            product_sell["Earning"] = product_sold*product.price
            product_sell['In Store'] = product.items_in_store
            # print(product_sell)
            all_my_products.append(product_sell)
       
        total_earning = sum(item['Earning'] for item in all_my_products)

        return {'products':product_queryset,'services':service_queryset,'orderitems':orderItem_queryset,
                'allProducts':all_my_products,"totalEarning":total_earning,
                "chart_data":chart_data_json,
                "line_chart_data":line_chart_data_json,
                "line_chart_price_data":line_chart_data_price_json,
                "pie_chart_price_data":pie_chart_data_price_json,
                "product_list":product_list,
                "chart_data_product":chart_data_product}
    


def get_products(request,offset):
    products = Product.objects.all()[offset:offset +12]
    data = [{'name':product.item_name,'image':product.image.url,
             'vendor':product.vendor.username}
             for product in products]
    return JsonResponse({'data':data})


def get_services(request,offset):
    services = Service.objects.all()[offset:offset +12]
    data = [{'name':service.item_name,'image':service.image.url,
             'vendor':str(service.vendor.username)} for service in services]
    return JsonResponse({'data':data})





# def index(request):
#     return render(request,'index.html')

def product_servict_list(request,category='products'):
    
    category = request.GET.get('category','products')
    print(category)

    products = Product.objects.all()
    services = Service.objects.all()

    #handle search logic
    search_query = request.GET.get('search',"")
    if search_query:
        search_filter = (
            Q(item_name__icontains =search_query)|
            Q(vendor__username__icontains = search_query)|
            Q(category__name__icontains = search_query)
        )
        products = products.filter(search_filter)
        services = services.filter(search_filter)

    #Handle price range filtering 
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)
        # services = services.filter(service_fee_gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
        # services = services.filter(service_fee__lte=max_price)

        
    
    return render(request,'vendors/index.html',
                  {'products':products,
                   'services':services,
                   'category':category})

