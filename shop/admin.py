from django.contrib import admin
from shop.models import Customer, Product, ProductImage, Cart, OrderPlaced, Payment

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['_user', 'name', 'created_at', 'address']
    search_fields = ['_user']
    ordering = ['customer_id', '_user', 'created_at']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_id', 'status', 'quantity', 'discount_price', 'rating']
    search_fields = ['title', 'status']
    ordering = ['product_id', 'status', 'discount_price', 'rating']

class CartAdmin(admin.ModelAdmin):
    list_display = ['product', '_user', 'quantity', 'added_at']
    search_fields = ['product', '_user']
    ordering = ['_user', 'quantity', 'added_at']

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['product','_customer', '_user',  'quantity', 'is_paid', 'status', 'ordered_at']
    search_fields = ['_user', 'product', 'status']
    ordering = ['_user', 'quantity', 'status', 'ordered_at']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', '_user', '_customer', 'method', 'amount', 'paid', 'due']
    search_fields = ['amount', 'paid', 'due']
    ordering = ['paid_at']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderPlaced, OrderPlacedAdmin)
admin.site.register(Payment, PaymentAdmin)