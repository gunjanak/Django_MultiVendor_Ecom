from django.contrib import admin

from vendors.models import (ProductCategory,ServiceCategory,Product,Service)

# Register your models here.


class ProductCategoryAdmin(admin.ModelAdmin):
    pass

class ServiceCategoryAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    list_display = ["item_name","vendor",
                    "category","items_in_store",
                    "price"]
    
    list_select_related = ["category"]
    search_fields = ["category"]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["item_name","vendor",
                    "category","is_active",
                    "pricing_type"]
    list_select_related = ["category"]
    search_fields = ["category","is_active"]

admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(ServiceCategory,ServiceCategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Service,ServiceAdmin)