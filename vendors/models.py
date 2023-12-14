from django.db import models
from accounts.models import CustomUser,CustomPermission

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class CommonFields(models.Model):
    vendor = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/',null=True,blank=True)

    class Meta:
        abstract = True

class Product(CommonFields):
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    items_in_store = models.IntegerField(null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)

class Service(CommonFields):
    category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    pricing_type = models.CharField(max_length=20,choices=[
        ('hourly','Hourly'),
        ('daily','Daily')
    ])
    hourly_rate = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    daily_rate = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
