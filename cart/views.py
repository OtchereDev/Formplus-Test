from django.shortcuts import render
from rest_framework.views import APIView
import json
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart, CartItem, PaymentTransaction

from cart.serializers import AddToCartSerializer, CartSerializer, GetCartResponse, GetCartSerializer
from products.models import Product
from drf_yasg.utils import swagger_auto_schema

from products.serializer import ErrorResponse, MessageResponse


# Create your views here.
class GetCartView(APIView):
    @swagger_auto_schema(responses={200: GetCartResponse(),404:ErrorResponse, 500:ErrorResponse,}, request_body=GetCartSerializer())
    def post(self, request):
        try:
            body =  json.loads(request.body)
            serializer = GetCartSerializer(data=body)

            if serializer.is_valid():
                cart = Cart.objects.get_or_create(user=serializer.data.get("email"))
                response_cart = CartSerializer(cart[0])
                message={
                    "message":"Cart successfully retrieved",
                    # "product":ProductSerializer(product).data
                    "cart":response_cart.data
                }
                return Response(data=message, status=status.HTTP_201_CREATED)
 
            else:
                response={
                    "errors":serializer.errors
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response={
                    "errors":str(e)
                }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddToCartView(APIView):
    @swagger_auto_schema(responses={200: MessageResponse(),404:ErrorResponse, 500:ErrorResponse,}, request_body=AddToCartSerializer())
    def post(self, request):
        try:
            body =  json.loads(request.body)
            serializer = AddToCartSerializer(data=body)

            if serializer.is_valid():
                cart = Cart.objects.get_or_create(user= serializer.data.get("email"))[0]
                product = Product.objects.get(product_id=serializer.data.get("products").get("product_id") )
                quantity=serializer.data.get("products").get("quantity") 
                try:
                    cart_item = cart.cart_items.get(cart=cart,product=product,)

                    if product.get_cart_or_sold_qunatity() > 0 and (((product.get_cart_or_sold_qunatity()-cart_item.quantity) + quantity) > product.quantity):
                        raise Exception("Item is either out of stock or the quantity available cannot fulfil this order ")
                    elif product.get_cart_or_sold_qunatity() <= 0 and (quantity > product.quantity):
                        raise Exception("Item is either out of stock or the quantity available cannot fulfil this order ")

                    cart_item.quantity = quantity
                    cart_item.save()
                except CartItem.DoesNotExist:
                    if (product.get_cart_or_sold_qunatity() +quantity) > product.quantity:
                        raise Exception("Item is either out of stock or the quantity available cannot fulfil this order ")

                    cart_item = CartItem.objects.create(quantity=quantity)
                   
                    cart_item.product.add(product)
                 
                    cart.cart_items.add(cart_item)
                    cart_item.save()
                   
               
                message={
                    "message":"Cart successfully updated",
                }
                return Response(data=message, status=status.HTTP_201_CREATED)
            else:
                response={
                    "errors":serializer.errors
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response={
                    "errors":str(e)
                }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentView(APIView):
    @swagger_auto_schema(responses={200: MessageResponse(),404:ErrorResponse, 500:ErrorResponse,}, request_body=GetCartSerializer())
    def post(self, request):
        try:
            body =  json.loads(request.body)
            serializer = GetCartSerializer(data=body)

            if serializer.is_valid():
                cart = Cart.objects.get(user= serializer.data.get("email"))
               
                if len(cart.cart_items.all()) == 0:
                    raise Exception("Cart does not contain any item to be purchased")

                
                cart_content = cart.cart_items.all()

                cart.cart_items.clear()

                payment_transaction = PaymentTransaction.objects.create(user=serializer.data.get("email"))
                payment_transaction.cart_items.add(*cart_content)
                    
                message={
                    "message":"Payment successfully made",
                }
                return Response(data=message, status=status.HTTP_201_CREATED)
            else:
                response={
                    "errors":serializer.errors
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            response={
                    "errors":["Cart for user not found"]
                }
            return Response(data=response, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            response={
                    "errors":str(e)
                }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
