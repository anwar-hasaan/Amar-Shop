from django.urls import path
from shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list.as_view(), name='products'),
    path('product/<product_id>/', views.product_details, name='product'),

    path('cart/', views.cart, name='cart'),
]
