from django.contrib import admin
from . models import Customer_Info, Product, Cart, OrderPlaced

# Register your models here.
@admin.register(Customer_Info)
class Customer_InfoAdmin(admin.ModelAdmin):
    list_display = ('name','id','division','district','thana','villorroad','zipcode')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','id','sellingprice','discountprice','description','brand','category','productimage')
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user','id','product','quantity')

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('user','id','Customer','product','quantity','orderdate','status')
    

    

