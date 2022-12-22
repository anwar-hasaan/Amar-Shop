from django.contrib import admin
from shop.models import Customer, Product, ProductImage, Cart, OrderPlaced, Payment

from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

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
    list_display = ['product', 'product_details', '_customer', '_user',  'quantity', 'is_paid', 'status', 'ordered_at']
    search_fields = ['_user', 'product', 'status']
    ordering = ['_user', 'quantity', 'status', 'ordered_at']

    def product_details(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:shop_product_change", args=(obj.product.pk,)),
            'see'
        ))
    product_details.short_description = 'product'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'show_user', 'show_customer', 'method', 'amount', 'paid', 'due', 'approved', 'show_orders']
    search_fields = ['amount', 'paid', 'due']
    ordering = ['paid_at']

    def show_user(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(obj._user.pk,)),
            obj._user.username
        ))
    def show_customer(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:shop_customer_change", args=(obj._customer.pk,)),
            obj._customer.name
        ))
    def show_orders(self, obj):
        all_products = [p.product for p in obj.orders.all()] # p is OrderPlaced object
        links = []
        for product in all_products:
            links.append(
                mark_safe('<a href="{}">{}</a>'.format(reverse("admin:shop_product_change", args=(product.pk,)), 
                product))
            )
        return format_html(' and '.join(links))
    show_user.short_description = 'User'
    show_customer.short_description = 'Customer'
    show_orders.short_description = 'Products'

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderPlaced, OrderPlacedAdmin)
admin.site.register(Payment, PaymentAdmin)