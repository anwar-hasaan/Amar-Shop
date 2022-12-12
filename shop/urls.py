from django.urls import path
from shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list.as_view(), name='products'),
    path('product/<pk>/', views.product_details.as_view(), name='product'),

    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<product_id>/', views.add_to_cart, name='addtocart'),
]
