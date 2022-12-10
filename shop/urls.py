from django.urls import path
from shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='products'),
    path('product/<product_id>/', views.product_details, name='product'),

    path('account/', views.account, name='account'),
    path('cart/', views.cart, name='cart'),
]
