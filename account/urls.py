from django.urls import path
from account import views

app_name = 'account'
urlpatterns = [
    path('', views.account, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('change-password/', views.change_password, name='change-password'),

    path('profile/', views.profile, name='profile'),
    path('add-address/', views.add_customer_address, name='add-address'),
]
