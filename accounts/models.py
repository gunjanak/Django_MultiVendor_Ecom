from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass

class CustomPermission(models.Model):
    pass

# Add a related_name to the user_permissions field
CustomUser._meta.get_field('user_permissions').related_name = 'custom_user_permissions'