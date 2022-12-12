from django.db import models
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

# Create your models here.

class CartItem(models.Model):
    product = models.ManyToManyField("products.Product")
    quantity = models.PositiveIntegerField()  

class Cart(models.Model):
    user= models.EmailField(max_length=255, )
    cart_items = models.ManyToManyField(CartItem,)

class PaymentTransaction(models.Model):
    user = models.EmailField(max_length=255, )
    cart_items = models.ManyToManyField(CartItem,)
