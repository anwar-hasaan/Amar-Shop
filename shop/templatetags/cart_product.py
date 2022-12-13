from django import template
from shop.models import Cart

register = template.Library()

@register.filter
def count_cart_product(user):
    try:
        all_cart_product = Cart.objects.filter(_user=user)
        if all_cart_product:
            count = 0
            for cart in all_cart_product:
                count += cart.quantity
            return count
    except Exception as e:
        pass
    return 0