# Generated by Django 4.2.7 on 2023-12-14 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_productcategory_servicecategory_service_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='category',
        ),
        migrations.RemoveField(
            model_name='service',
            name='vendor',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='ServiceCategory',
        ),
    ]
