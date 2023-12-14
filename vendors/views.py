from typing import Any
from django import http
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView
from django.http import Http404


from vendors.models import Product,Service
from vendors.forms import ProductForm, ServiceForm


# Create your views here.

class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = "create_product.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        return super().form_valid(form)

class ServiceCreateView(LoginRequiredMixin,CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "create_service.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        return super().form_valid(form)




class ProductServiceListView(ListView):
    model = Product
    template_name = "product_service_list.html"
    context_object_name = "product_service_list"

    def get_queryset(self):
        return Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_list'] = Service.objects.all()
        return context
    

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

class ServiceDetailView(DetailView):
    model = Service
    template_name = "service_detail.html"
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
    template_name = "edit_product.html"
    success_url = reverse_lazy("home")

class ServiceUpdateView(VendorRequiredMixin,UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "edit_service.html"
    success_url = reverse_lazy('home')


class ProductDeleteView(VendorRequiredMixin,DeleteView):
    model = Product
    context_object_name = "product"
    template_name = "delete_product.html"
    success_url = reverse_lazy("home")

class ServiceDeleteView(VendorRequiredMixin,DeleteView):
    model = Service
    context_object_name = "service"
    template_name = "delete_service.html"
    success_url = reverse_lazy("home")

class UserProductServiceListView(LoginRequiredMixin,ListView):
    template_name = "user_product_service_list.html"
    context_object_name = "user_product_service_list"

    def get_queryset(self):
        user = self.request.user
        product_queryset = Product.objects.filter(vendor=user)
        service_queryset = Service.objects.filter(vendor = user)
        return {'products':product_queryset,'services':service_queryset}
    
