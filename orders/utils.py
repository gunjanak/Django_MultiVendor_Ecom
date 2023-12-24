from orders.models import Order, OrderItem
from vendors.models import CustomUser,Product

def VendorShop(order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        print(item.product.item_name)
        ##Decrease the sold amount
        item.product.items_in_store = item.product.items_in_store - item.quantity
        print(item.product.items_in_store)
        item.product.save()