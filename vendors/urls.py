from django.urls import path
from vendors.views import (ProductCreateView, ServiceCreateView, ProductServiceListView,
                           ProductDetailView,ServiceDetailView,ProductUpdateView,ServiceUpdateView,
                           ProductDeleteView,ServiceDeleteView,UserProductServiceListView,
                           index,get_products,get_services,product_list,service_list)


urlpatterns = [
    path("create_product/",ProductCreateView.as_view(),name="create_product"),
    path("create_service/",ServiceCreateView.as_view(),name='create_service'),
    # path("",ProductServiceListView.as_view(),name="home"),
    path("product/<int:pk>/",ProductDetailView.as_view(),name="product_detail"),
    path("service/<int:pk>/",ServiceDetailView.as_view(),name="service_detail"),
    path("product/<int:pk>/edit/",ProductUpdateView.as_view(),name="edit_product"),
    path("service/<int:pk>/edit/",ServiceUpdateView.as_view(),name="edit_service"),
    path("product/<int:pk>/delete/",ProductDeleteView.as_view(),name="delete_product"),
    path("service/<int:pk>/delete/",ServiceDeleteView.as_view(),name="delete_service"),
    path("user-product-service-list/",UserProductServiceListView.as_view(),
         name='user_product_service_list'),
    # path("",index,name=index),
    path('get_products/<int:offset>/',get_products,name='get_products'),
    path('get_services/<int:offset>/',get_services,name='get_services'),
    path('products/',product_list,name='product_list'),
    path('services/',service_list,name="service_list"),
    path("",index,name="home"),



]
