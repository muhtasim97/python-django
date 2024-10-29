from django.db import models
from .customer import Customer
from .product import Product
import datetime
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    address=models.CharField(max_length=50,default='',blank=True)
    phone=models.CharField(max_length=50,default='',blank=True)
    quantity=models.IntegerField(default=1)
    date=models.DateTimeField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    def order_save(self):
        self.save()


    @staticmethod
    def order_list(customer_id):
        return Order.objects.filter(customer=customer_id)