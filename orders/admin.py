from django.contrib import admin
from django.http import HttpResponse

import csv
import datetime

from orders.models import Order,OrderItem
from orders.utils import VendorShop

# Register your models here.

@admin.action(description="Paid Done")
def payment_done(ModelAdmin,request,queryset):
    print(Order)
    queryset.update(paid=True)

    #Retrieve and print the orders for which the action has been applied
    updated_orders = Order.objects.filter(id__in=queryset.values_list('id',flat=True))
    for order in updated_orders:
        print(order.id)
        VendorShop(order.id)


def export_to_csv(ModelAdmin,request,queryset):
    opts = ModelAdmin.model._meta
    content_disposition= f'attachement;filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    #Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])

    #write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj,field.name)
            if isinstance(value,datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)

        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to csv'





class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','address','postal_code','city','paid','created','updated']
    list_filter = ['paid','created','updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv,payment_done]

