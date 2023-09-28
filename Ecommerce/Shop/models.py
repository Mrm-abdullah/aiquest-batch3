from django.db import models
from django.contrib.auth.models import User

# Create your models here.
DIVITION_CHOICES = (
        ('Dhaka','Dhaka'),
        ('Rangpur','Rangpur'),
        ('Rajshahi','Rajshahi'),
        ('Khulna','Khulna'),
        ('Barisal','Barisal'),
        ('Chattogram','Chattogram'),
        ('Mymenshing','Mymenshing'),
        ('Sylhet','Rajshahi'),
    )

class Customer_Info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    division = models.CharField(choices=DIVITION_CHOICES, max_length=50)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=50)
    villorroad = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES = (
        ('GP','Gents Pant'),
        ('B','Borkha'),
        ('BF','Baby Fashion'),
        ('S','Sharee'),
        ('L','Lehegga'),
    )

class Product(models.Model):
    title = models.CharField(max_length=100)
    sellingprice = models.FloatField()
    discountprice = models.FloatField()
    description = models.TextField()
    brand = models.CharField( max_length=100)
    category = models.CharField(choices= CATEGORY_CHOICES, max_length=2)
    productimage = models.ImageField(upload_to='productimage')

    def __str__(self):
        return str(self.id)
        
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discountprice

STATUS_CHOICE = (
        ('Pending','Pending'),
        ('Acceptead','Acceptead'),
        ('Packed','Packed'),
        ('on the way','on the way'),
        ('Delivered','Delivered'),
        ('Cancel','Cancel'),
    )

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer_Info, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    orderdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices= STATUS_CHOICE, max_length=50, default='Pending')
    
    def __str__(self):
        return str(self.id)

    
    @property
    def total_cost(self):
        return self.quantity * self.product.discountprice