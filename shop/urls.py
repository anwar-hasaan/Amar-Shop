from django.urls import path
from shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list.as_view(), name='products'),
    path('product/<pk>/', views.product_details.as_view(), name='product'),

    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<product_id>/', views.add_to_cart, name='addtocart'),
    path('increase-cart-item/', views.increase_item, name='increase-item'),
    path('decrease-cart-item/', views.decrease_item, name='decrease-item'),
    path('remove-cart-item/', views.remove_cart_item, name='remove-item'),

    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
]
