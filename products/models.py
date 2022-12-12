from django.db import models
import uuid
from django.core.validators import MinValueValidator

from cart.models import CartItem 
import functools


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=8)
    labels= models.ManyToManyField("ProductLabel")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    product_id=models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True)

    def get_out_of_stock(self):
        return self.get_cart_or_sold_qunatity() >= self.quantity

    def get_available_stock_quantity(self):
        return self.quantity - self.get_cart_or_sold_qunatity() 

    def get_cart_or_sold_qunatity(self):
        total_quant=0
        for item in CartItem.objects.filter(product=self.product_id):
            total_quant+=item.quantity 
        return total_quant
       

class ProductLabel(models.Model):
    name = models.CharField(max_length=225)
    value= models.CharField(max_length=225)