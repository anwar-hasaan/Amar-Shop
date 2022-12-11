from django.contrib import admin
from shop.models import Customer, Product, ProductImage, Cart, OrderPlaced

class CustomerAdmin(admin.ModelAdmin):
    list_display = []

class ProductAdmin(admin.ModelAdmin):
    list_display = []

class CartAdmin(admin.ModelAdmin):
    list_display = []

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = []

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(OrderPlaced)