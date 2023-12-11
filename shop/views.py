from django import http
from .models import Category, Product, ReviewItem, Cart, CartItem, Checkout, Orders
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import HttpRequest
from blog.models import Blog, Department
from typing import Any

class HomeTemplateView(TemplateView):
    template_name = 'shop/home.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured'] = Product.objects.all()
        context['latest_products'] = Product.objects.order_by('-post_date')[:3]
        context['ratings'] = Product.objects.order_by("-rating")[:3]
        context['reviews'] = ReviewItem.objects.order_by("-likes")[:3]
        context['blogs'] = Blog.objects.order_by('-created_on')[:3]
        return context

@method_decorator(login_required, name='dispatch')
class ShopTemplateView(TemplateView):
    template_name = "shop/shop.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.user = request.user
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['latest_products'] = Product.objects.order_by('-post_date')[:3]
        context['discounts'] = Product.objects.order_by("-discount")[:10]
        context['product_count'] = Product.objects.count()
        context['products'] = Product.objects.all()
        cart, created = Cart.objects.get_or_create(user=self.user)
        if created:
            cart.save()
            context['cart_item_count'] = CartItem.objects.filter(cart=cart).count()
        context['grand_total'] = cart.grand_total()
        return context
    
@method_decorator(login_required, name='dispatch')
class ShopDetailTemplateView(TemplateView):
    template_name = 'shop/product_detail.html'

    def get(self, request: HttpRequest, product_id, *args: Any, **kwargs: Any) -> HttpResponse:
        self.user = request.user
        self.product = get_object_or_404(Product, pk=product_id)
        return super().get(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, product_id):
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST['quantity'])
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
            product.quantity -= 1
            product.save()

        return redirect("product_details",product_id)
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        context['review_count'] = ReviewItem.objects.filter(product=self.product).count()
        context['reviews'] = ReviewItem.objects.filter(product=self.product)
        context['related_products'] = Product.objects.filter(category=self.product.category)[:4]
        cart = Cart.objects.get(user=self.user)
        context['cart_item_count'] = CartItem.objects.filter(cart=cart).count()
        context['grand_total'] = cart.grand_total()
        if self.product.quantity != 0:
            context['product_availability'] = "In Stock"
        else:
            context['product_availability'] = "Depleted"
        return context
    
@method_decorator(login_required, name='dispatch')
class ShoppingCartTemplateView(TemplateView):
    template_name = 'shop/shopping_cart.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.user = request.user
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.user)
        context['cart_item_count'] = CartItem.objects.filter(cart=cart).count()
        context['cart_items'] = CartItem.objects.filter(cart=cart)
        context['grand_total'] = cart.grand_total()
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.cartitem_set.all()

        # Handle quantity update
        for item in cart_items:
            new_quantity = request.POST.get(f'quantity_{item.id}')
            if new_quantity:
                item.quantity = int(new_quantity)
                item.save()
        
        # Handle item removal
        item_id_to_remove = request.POST.get('remove_item')
        if item_id_to_remove:
            item_to_remove = get_object_or_404(CartItem, id=item_id_to_remove)
            item_to_remove.delete()
        
        return redirect('shopping_cart')
    
@method_decorator(login_required, name='dispatch')
class CheckoutTemplateView(TemplateView):
    template_name = "shop/checkout.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.user = request.user
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.user)
        if created:
            cart.save()
        context['user'] = self.user
        context['cart_item_count'] = CartItem.objects.filter(cart=cart).count()
        context['cart_items'] = CartItem.objects.filter(cart=cart)
        context['grand_total'] = cart.grand_total()
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.cartitem_set.all()
        fname = request.POST['fname']
        lname = request.POST['lname']
        county = request.POST['county']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        post_code = request.POST['postcode']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        order_note = request.POST['order_note']
        paid_amount = cart.grand_total()

        # Details for checkout table
        checkout = Checkout.objects.create(first_name=fname,
                                                    last_name=lname,
                                                    user=request.user,
                                                    county=county,
                                                    address1=address1,
                                                    address2=address2,
                                                    city=city,
                                                    post_code=post_code,
                                                    phone_number=phone_number,
                                                    email=email,
                                                    order_note=order_note,
                                                    paid_amount=paid_amount)
        checkout.save()
        
        # Details for order table
        for item in cart_items:
            order = Orders.objects.create(user=request.user,
                                      product=item.product,
                                      checkout=checkout,
                                      delivered=0)
            order.save()
            item.delete()

        return redirect("checkout")