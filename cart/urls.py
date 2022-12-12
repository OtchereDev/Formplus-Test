from django.urls import path

from cart.views import AddToCartView, GetCartView, PaymentView

app_name='cart'

urlpatterns = [
    path("get-cart", GetCartView().as_view()),
    path("add-cart", AddToCartView().as_view()),
    path("payment", PaymentView().as_view())

]
