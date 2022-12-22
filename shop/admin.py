from django.contrib import admin
from django.contrib.auth.models import Group
from shop.models import Customer, Product, ProductImage, Cart, OrderPlaced, Payment

from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['_user', 'name', 'created_at', 'address']
    search_fields = ['_user']
    ordering = ['customer_id', '_user', 'created_at']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'show_prod_images', 'status', 'quantity', 'discount_price', 'rating']
    search_fields = ['title', 'status']
    ordering = ['product_id', 'status', 'discount_price', 'rating']

    def show_prod_images(self, obj):
        all_images = [image for image in obj.image.all()] 
        links = []
        for count, image in enumerate(all_images, start=1):
            links.append(
                mark_safe('<a target="_blank" href="{}">{}</a>'.format(image.get_url, f'img {count}'))
            )
            
        return format_html(', '.join(links))
    show_prod_images.short_description = 'images'

class CartAdmin(admin.ModelAdmin):
    list_display = ['product', '_user', 'quantity', 'added_at']
    search_fields = ['product', '_user']
    ordering = ['_user', 'quantity', 'added_at']

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_details', 'show_prod_images', '_customer', '_user',  'quantity', 'is_paid', 'status', 'ordered_at']
    search_fields = ['_user', 'product', 'status']
    ordering = ['_user', 'quantity', 'status', 'ordered_at']

    def product_details(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:shop_product_change", args=(obj.product.pk,)),
            'see'
        ))
    def show_prod_images(self, obj):
        all_images = [image for image in obj.product.image.all()] # p is OrderPlaced object
        links = []
        for count, image in enumerate(all_images, start=1):
            links.append(
                mark_safe('<a target="_blank" href="{}">{}</a>'.format(image.get_url, f'img {count}'))
            )
            
        return format_html(', '.join(links))
    show_prod_images.short_description = 'images'
    product_details.short_description = 'product'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'show_user', 'show_customer', 'method', 'amount', 'paid', 'due', 'approved', 'show_orders', 'all_orders_with_this_pay']
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

    # show all orderplaced obj with this payment obj
    def all_orders_with_this_pay(self, obj):
        url = (
            reverse("admin:shop_orderplaced_changelist")
            + "?pk__in=" 
            + ",".join([str(order.pk) for order in obj.orders.all()])
        )
        return format_html('<a href="{}">{}</a>', url, 'orders')
    show_user.short_description = 'User'
    show_customer.short_description = 'Customer'
    show_orders.short_description = 'Products'
    all_orders_with_this_pay.short_description = 'Orders'

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderPlaced, OrderPlacedAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.unregister(Group)