from django.contrib import admin
from .models import Product, Category, Review, ReviewItem, CartItem, Cart, Orders, Checkout

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ReviewItem)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(Checkout)