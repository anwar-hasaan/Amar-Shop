from django.shortcuts import render
from django.views.generic import ListView, DetailView
from shop.models import Product

def home(request):
    return render(request, 'shop/home.html')

class product_list(ListView):
    model = Product
    paginate_by = 12
    template_name = 'shop/products.html'

def product_details(request, product_id):
    return render(request, 'shop/product_details.html')

def cart(request):
    return render(request, 'shop/cart.html')