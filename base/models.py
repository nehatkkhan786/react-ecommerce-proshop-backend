from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to ='uploads/')
    brand = models.CharField(max_length=200,null=True, blank=True )
    category = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(default=0, null=True, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(default=0, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    _id = models.AutoField(primary_key=True, editable=False)


    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(f'{self.name} + - {self.product.name} ')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=200, blank=True, null=True)
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False, null=True, blank=True)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False, null=True, blank=True)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.createdAt)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True )
    name = models.CharField(max_length=200, blank=True, null=True)
    qty = models.CharField(max_length=200, null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, null=True, blank=True )
    city = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)


    def __str__(self):
        return self.address