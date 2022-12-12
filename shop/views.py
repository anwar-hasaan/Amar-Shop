from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from shop.models import Product, Cart, Customer, OrderPlaced
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'shop/home.html')

class product_list(ListView):
    model = Product
    paginate_by = 3
    ordering = 'product_id'
    template_name = 'shop/products.html'

class product_details(DetailView):
    model = Product
    template_name = 'shop/product_details.html'

@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(_user=user, is_ordered=False)
    for cart in cart_products:
        print(cart.product.title)
    context = {
        'carts': cart_products
    }
    return render(request, 'shop/cart.html', context)

def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.filter(product_id=product_id).first()
    if product:
        cart_products = Cart.objects.filter(_user=user, is_ordered=False)
        cart_products = [cart._product for cart in cart_products]
        if product in cart_products:
            print('in cart')
            in_cart = Cart.objects.get(product=product)
            in_cart.quantity += 1
            in_cart.save()
            print('quantity increased')
        else:
            cart = Cart.objects.create(_user=user, product=product)
            cart.save()
            print('product added')

        
        
    return render(request, 'shop/cart.html')