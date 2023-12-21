from django.contrib import admin
from accounts.models import CustomUser


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser,CustomUserAdmin)