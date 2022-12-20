from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from shop.models import Product, Cart, Customer, OrderPlaced, Payment
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    # showing user cart, products and cost info
    user = request.user
    cart_products = Cart.objects.filter(_user=user)
    sub_total_cost = 0
    for cart in cart_products:
        sub_total_cost += cart.get_sub_total

    CUSTOMERS = Customer.objects.filter(_user=user)
            
        
    context = {
        'carts': cart_products,
        'shiping': SHIPING_CHARGE,
        'sub_total': sub_total_cost,
        'total_cost': sub_total_cost+SHIPING_CHARGE,
        'customers': CUSTOMERS,
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

@login_required
def checkout(request):
    user = request.user
    if request.method == 'POST':
        cus_id = request.POST.get('customer-id')

        customer = Customer.objects.filter(customer_id=cus_id).first()
        if customer:
            all_cart_prods = Cart.objects.filter(_user=user)

            if all_cart_prods:
                total_regular_price = 0
                total_discount = 0
                total_quantity = 0
                sub_total_cost = 0

                for cart in all_cart_prods:
                    total_regular_price += cart.product.regular_price
                    total_discount += cart.product.discount
                    total_quantity += cart.quantity
                    sub_total_cost += cart.product.discount_price

                    order_place = OrderPlaced.objects.create(_user=user, _customer=customer, 
                                product=cart.product, quantity=cart.quantity)
                    order_place.save()
                    cart.delete()

                context = {
                    'reqular_price': total_regular_price,
                    'total_discount': total_discount,
                    'total_quantity': total_quantity,
                    'sub_total_cost': sub_total_cost,
                    'total_cost': sub_total_cost + SHIPING_CHARGE,
                    'shiping_charge': SHIPING_CHARGE,
                }
                messages.success(request, 'Order placed, select payment to confirm order!')
                return render(request, 'shop/payment_method.html', context)

            messages.error(request, 'No Products in Cart!')
            return redirect('/cart')
        messages.error(request, 'Invalid Address!')    
    return redirect('/cart')


@login_required
def payment(request):
    user = request.user
    total_cost = 0
    
    if request.method == 'POST':
        placed_order = OrderPlaced.objects.filter(_user=user, is_paid=False)
        if 'cod' in request.POST:
            payment = Payment.objects.create(method='cod')
            if placed_order:
                for order in placed_order:
                    total_cost += order.total_amount
                    payment.orders.add(order)
                    
                    order.is_paid = True
                    order.save()
                total_cost = total_cost + SHIPING_CHARGE
                payment.amount = total_cost
                payment.due = total_cost
                payment.paid = 0
                payment.save()
                messages.success(request, 'Order confirmed, you can pay at home.')
                return redirect('/account/profile')
            
            messages.error(request, 'No products on Placed order!')
            return redirect('/account/profile')
            
        elif 'bkash' in request.POST:
            pass
        elif 'nagad' in request.POST:
            pass

    return render(request, 'shop/payment_method.html')