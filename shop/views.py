from django.shortcuts import render
from django.views.generic import ListView, DetailView

def account(request):
    return render(request, 'shop/account.html')

def home(request):
    return render(request, 'shop/home.html')

def product_list(request):
    return render(request, 'shop/products.html')

def product_details(request, product_id):
    return render(request, 'shop/product_details.html')

def cart(request):
    return render(request, 'shop/cart.html')