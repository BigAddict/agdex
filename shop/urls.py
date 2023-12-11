from django.urls import path
from .views import HomeTemplateView, ShopTemplateView, ShopDetailTemplateView, ShoppingCartTemplateView, CheckoutTemplateView

urlpatterns = [
    path("", HomeTemplateView.as_view(), name='home'),
    path("shop/", ShopTemplateView.as_view(), name='shop'),
    path("product_detail/<int:product_id>/", ShopDetailTemplateView.as_view(), name='product_details'),
    path("shopping_cart/", ShoppingCartTemplateView.as_view(), name='shopping_cart'),
    path("checkout", CheckoutTemplateView.as_view(), name="checkout")
]
