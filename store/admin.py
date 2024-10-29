from django.contrib import admin
from .models.product import Product
from .models.catagory import Category
from .models.customer import Customer
from .models.orders import Order

class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category','description']
class AdminCategory(admin.ModelAdmin):
    list_display=['name']
class AdminCustomer(admin.ModelAdmin):
    list_display=['firstname','lastname','phone','email','password']   
class AdminOrder(admin.ModelAdmin):
    list_display=['customer','product','address','phone','quantity']     
# Register your models here.
admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Order,AdminOrder)