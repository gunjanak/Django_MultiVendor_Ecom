from django.urls import path

from orders.views import order_create_view,OrderPDFView

app_name = "orders"

urlpatterns = [
    path('create/',order_create_view,name="order_create"),
    path('order/<int:pk>/pdf/',OrderPDFView.as_view(),name="order_pdf"),
]