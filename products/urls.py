from django.urls import path
from products.views import ProductView, ProductViewWithId

app_name='products'

urlpatterns = [
    path("products", ProductView.as_view()),
    path("products/<uuid:id>", ProductViewWithId.as_view()),
]
