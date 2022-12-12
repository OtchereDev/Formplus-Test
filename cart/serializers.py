from rest_framework import serializers

from cart.models import Cart, CartItem
from products.models import Product
from products.serializer import ProductSerializer


class GetCartSerializer(serializers.Serializer):
    email= serializers.EmailField(required=True)

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    class Meta:
        fields=["quantity", "product"]
        model= CartItem
    

class CartSerializer(serializers.ModelSerializer):   
    cart_items = CartItemSerializer(many=True)
    class Meta:
        fields=["user", "cart_items"]
        model= Cart


class AddToCartItemSerializer(serializers.Serializer):
    quantity= serializers.IntegerField(min_value=0)
    product_id= serializers.PrimaryKeyRelatedField(queryset= Product.objects.all())

class AddToCartSerializer(serializers.Serializer):
    email = serializers.EmailField()
    products = AddToCartItemSerializer()
    

class GetCartResponse(serializers.Serializer):
    cart = CartSerializer()
    message=serializers.CharField(required=False)

