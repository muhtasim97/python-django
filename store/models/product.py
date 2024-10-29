from django.db import models
from .catagory import Category

class Product(models.Model):
    name=models.CharField(max_length=20)
    price=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=200, default='',blank=True,null=True)
    image=models.ImageField(upload_to='product_img/')

    @staticmethod
    def get_all_product_data():
        return Product.objects.all()

    @staticmethod
    def get_all_product_data_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_product_data()
    
    @staticmethod
    def product_info(listofproducts):
        return Product.objects.filter(id__in=listofproducts)
