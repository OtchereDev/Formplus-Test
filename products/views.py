from django.shortcuts import render
from rest_framework.views import APIView
from products.models import Product
from products.serializer import ErrorResponse, MessageResponse, ProductResponse, ProductSerializer,AllProductResponse
from rest_framework.response import Response
from rest_framework import status
import json
from drf_yasg.utils import swagger_auto_schema



# Create your views here.
class ProductView(APIView):
    @swagger_auto_schema(responses={200: AllProductResponse()})
    def get(self, request, *args, **kwargs):
        all_products = Product.objects.all()
        products_serialized = ProductSerializer(all_products, many=True)
        products={
            "message":"Successfully fetched all products",
            "products":products_serialized.data
        }
        return Response(data=products, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: ProductResponse(), 400:ErrorResponse, 500:ErrorResponse,},request_body=ProductSerializer())
    def post(self,request):
        try:
            body =  json.loads(request.body)
            serializer = ProductSerializer(data=body)
            
            if serializer.is_valid():
                product = serializer.save()
                message={
                    "message":"Product successfully created",
                    "product":ProductSerializer(product).data
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



class ProductViewWithId(APIView):
    @swagger_auto_schema(responses={204: MessageResponse,404:ErrorResponse, 500:ErrorResponse,})
    def delete(self, request, *args, **kwargs):
        product_id = kwargs["id"]
        try:
            product =Product.objects.get(product_id=product_id)
            product.delete()
            response = {
                "message": "Successfully Deleted Products"
            }
            return Response(data=response, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            response = {
                "errors":"Product not found"
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "errors": str(e)
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(responses={200: ProductResponse(),404:ErrorResponse, 500:ErrorResponse,})
    def get(self, request, *args, **kwargs):
        product_id = kwargs["id"]

        try:
            product =Product.objects.get(product_id=product_id)
            searializer = ProductSerializer(product)
            response = {
                "product":searializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            response = {
                "errors":"Product not found"
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "errors": str(e)
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(responses={200: ProductResponse(), 400:ErrorResponse, 500:ErrorResponse,},request_body=ProductSerializer())
    def patch(self,request,*args, **kwargs):
        try:
            product_id = kwargs["id"]

            product =Product.objects.get(product_id=product_id)
            body =  json.loads(request.body)

            serializer = ProductSerializer(product, data=body, partial=True)

            if serializer.is_valid():
                product = serializer.save()
                message={
                    "message":"Product successfully updated",
                    "product":ProductSerializer(product).data
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
    
   
