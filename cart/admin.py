from django.contrib import admin

from cart.models import Cart, CartItem, PaymentTransaction

# Register your models here.
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(PaymentTransaction)