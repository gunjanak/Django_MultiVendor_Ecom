from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pic/',blank=True,null=True)
    first_name = models.CharField(max_length=50,blank=True) 
    last_name = models.CharField(max_length=50,blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=250,blank=True)
    postal_code= models.CharField(max_length=20,blank=True)
    city = models.CharField(max_length=20,blank=True)


    def __str__(self):
        return self.user.username