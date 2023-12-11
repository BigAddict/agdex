from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='product_photos/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    
    def discounted_price(self):
        discount_factor = 1 - (self.discount / 100)
        discounted_price = float(self.price) * discount_factor
        return round(discounted_price, 2)

class Review(models.Model):
    product = models.ManyToManyField(Product, through='ReviewItem')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self) -> str:
        return f"Review {self.pk}"
    
class ReviewItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    review_date = models.DateField(auto_now_add=True)
    review_text = models.TextField()
    likes = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"Review on {self.product.name} by {self.review.user.username}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='CartItem')

    def grand_total(self):
        total = sum(item.product.price * item.quantity for item in self.cartitem_set.all())
        return round(total, 2)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        total_price = self.product.price * self.quantity
        return round(total_price, 2)

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product.name}"
    
class Checkout(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    county = models.CharField(max_length=20)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=15)
    post_code = models.CharField(max_length=15)
    phone_number = models.PositiveIntegerField()
    email = models.CharField(max_length=100)
    order_note = models.CharField(max_length=200)
    checkout_date = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.user.username} Order {self.pk}"
    
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField()

    def __str__(self) -> str:
        return f"Order for {self.user.username} on {self.order_date}"