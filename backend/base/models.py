from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    # In order to use Image Fiend we have to use pillow-> pip file
    image = models.ImageField(null = True, blank=True)
    brand = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        # to see the product name at the admin panel
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, max_length=200,
                             on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)


class Order(models.Model):
    user = models.ForeignKey(User, max_length=200,on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(null=False, default= False)
    paidAt = models.DateTimeField(auto_now_add= False, null = True, blank = True)
    isDelivered = models.BooleanField(null=False, default= False)
    deliveredAt = models.DateTimeField(auto_now_add= False, null = True, blank = True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.createdAt)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, max_length=200,on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, max_length=200,on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, max_length=200,on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null= True, blank = True, default = 0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return self.name

class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, max_length=200,on_delete=models.SET_NULL, null=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.IntegerField( null = True, blank = True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shhippingPrice =  models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.address
