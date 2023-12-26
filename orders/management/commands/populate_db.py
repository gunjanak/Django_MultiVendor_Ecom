import random
from datetime import datetime,timedelta
from django.utils import timezone
from typing import Any
import pytz
from django.core.management.base import BaseCommand

from vendors.models import Product
from orders.models import Order,OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        first_name=['Harry',"Rita","Mita","Nita","Aastha",
                    "Sushma","Shovita","Sunita","Silu","Kritika"]
        last_name = ["GC","KC","Newa","Thapa","Karki","Sharma","Bhatta"]

        address =["123 Main Street","595 Machindra Marg","896 RamShah Path","456 Telostoy Road","12 Kafka Road"]
        postal_code = ["31000","57000","80331","90331","52662","150000","341000"]
        city = ["Toulouse","Bhojpur","Munich","Oleshnyk","Oblast","Petropavl","Ganzhou"]
        


        for i in range(100):
            start_date = datetime.strptime('2023-01-01 12:30:30','%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime('2023-12-24 12:30:30','%Y-%m-%d %H:%M:%S')
            random_time = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
            # print(random_time)
            order = Order.objects.create(
                first_name = random.choice(first_name),
                last_name = random.choice(last_name),
                email = "abc@abc.com",
                address = random.choice(address),
                postal_code = random.choice(postal_code),
                city = random.choice(city),
                created= timezone.make_aware(random_time),
                updated = timezone.make_aware(random_time),
                paid= False)
            
            try:
                product1 = Product.objects.get(pk = random.randint(26,32))
                OrderItem.objects.create(order=order,product=product1,price=product1.price,quantity=random.randint(1,15))
                product2 = Product.objects.get(pk = random.randint(24,32))
                OrderItem.objects.create(order=order,product=product2,price=product2.price,quantity=random.randint(1,15))
                product3 = Product.objects.get(pk = random.randint(23,32))
                OrderItem.objects.create(order=order,product=product3,price=product3.price,quantity=random.randint(1,15))
            
                order.save()
                print(order)
            except:
                pass
            
        self.stdout.write(self.style.SUCCESS("Successfully populated the database."))

