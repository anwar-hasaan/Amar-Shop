from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from shop.models import Product, Cart, Customer, OrderPlaced
from django.contrib.auth.decorators import login_required

from account.utails import login_using_session

SHIPING_CHARGE = 50

def home(request):
    if not request.user.is_authenticated:
        login_using_session(request=request)
    latest = Product.objects.filter(status='lastest')
    featured = Product.objects.filter(status='featured')
    exclusive = Product.objects.filter(status='exclusive').first()
    
    context = {
        'latest': latest,
        'featured': featured,
        'exclusive': exclusive
    }
    return render(request, 'shop/home.html', context)

class product_list(ListView):
    model = Product
    paginate_by = 4
    ordering = 'product_id'
    template_name = 'shop/products.html'

class product_details(DetailView):
    model = Product
    template_name = 'shop/product_details.html'

@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(_user=user)
    sub_total_cost = 0
    for cart in cart_products:
        sub_total_cost += cart.get_sub_total
    context = {
        'carts': cart_products,
        'shiping': SHIPING_CHARGE,
        'sub_total': sub_total_cost,
        'total_cost': sub_total_cost+SHIPING_CHARGE
    }
    return render(request, 'shop/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.filter(product_id=product_id).first()
    if product:
        cart_products = Cart.objects.filter(_user=user)
        cart_products = [cart.product for cart in cart_products]
        if product in cart_products:
            in_cart = Cart.objects.get(product=product)
            in_cart.quantity += 1
            in_cart.save()
        else:
            cart = Cart.objects.create(_user=user, product=product)
            cart.save()
    return redirect('/cart')
    
@login_required
def increase_item(request):
    user = request.user
    product_id = request.GET.get('product_id')
    c = Cart.objects.get(product__product_id=product_id, _user=user)
    if c.quantity < 10:
        c.quantity += 1
        c.save()
    
    sub_total = 0
    cart_quantity = 0
    for cart in Cart.objects.filter(_user=user):
        sub_total += cart.get_sub_total
        cart_quantity += cart.quantity
    
    data = {
        'all_prod_subtotal_cost': sub_total,
        'all_prod_total_cost': sub_total + SHIPING_CHARGE,
        'sub_total': c.get_sub_total,
        'quantity': c.quantity,
        'cart_quantity': cart_quantity
    }
    return JsonResponse(data)

@login_required
def decrease_item(request):
    user = request.user
    product_id = request.GET.get('product_id')
    c = Cart.objects.get(product__product_id=product_id, _user=user)
    if c.quantity > 1:
        c.quantity -= 1
        c.save()
    
    sub_total = 0
    cart_quantity = 0
    for cart in Cart.objects.filter(_user=user):
        sub_total += cart.get_sub_total
        cart_quantity += cart.quantity
    data = {
        'all_prod_subtotal_cost': sub_total,
        'all_prod_total_cost': sub_total + SHIPING_CHARGE,
        'sub_total': c.get_sub_total,
        'quantity': c.quantity,
        'cart_quantity': cart_quantity
    }
    return JsonResponse(data)

@login_required
def remove_cart_item(request):
    user = request.user
    product_id = request.GET.get('product_id')
    c = Cart.objects.get(product__product_id=product_id, _user=user)
    c.delete()
    
    sub_total = 0
    cart_quantity = 0
    for cart in Cart.objects.filter(_user=user):
        sub_total += cart.get_sub_total
        cart_quantity += cart.quantity
    data = {
        'all_prod_subtotal_cost': sub_total,
        'all_prod_total_cost': sub_total + SHIPING_CHARGE,
        'cart_quantity': cart_quantity
    }
    return JsonResponse(data)