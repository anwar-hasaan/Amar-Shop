from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from shop import utails

class Customer(models.Model):
    customer_id = models.CharField(max_length=20, primary_key=True, unique=True, blank=True)
    _user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    district = models.CharField(max_length=20, choices=utails.DISTRICT_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=20, choices=utails.CITY_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()

    def save(self,*args,**kwargs):
        if not self.customer_id:
            self.customer_id = BaseUserManager().make_random_password(6)
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to=utails.get_upload_dir)
    @property
    def get_url(self):
        return f"/media/{self.image}"
    def __str__(self):
        name_list = str(self.image.path).split('\\')
        return name_list[-1]

class Product(models.Model):
    product_id = models.CharField(max_length=20, primary_key=True, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=utails.PRODUCT_CATEGORY, null=True, blank=True)
    title = models.CharField(max_length=250)
    model = models.CharField(max_length=250, null=True, blank=True)
    image = models.ManyToManyField(ProductImage)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=utails.PRODUCT_STATUS, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    regular_price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField()
    rating = models.FloatField(default=5.0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    def discount(self):
        return self.regular_price - self.discount_price
    def is_available(self):
        return True if self.quantity >= 1 else False
    def save(self,*args,**kwargs):
        if not self.product_id:
            self.product_id = BaseUserManager().make_random_password(6)
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class Cart(models.Model):
    _user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_sub_total(self):
        return self.quantity * self.product.discount_price
    def __str__(self):
        return self.product.title

class OrderPlaced(models.Model):
    _user = models.ForeignKey(User, on_delete=models.CASCADE)
    _customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    paid_amount = models.PositiveIntegerField(null=True, blank=True)
    due_amount = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=utails.ORDER_STATUS, default=utails.ORDER_STATUS[0])
    ordered_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_deliverd(self):
        return True if self.status == 'deliverd' else False
    def __str__(self):
        return self.product.title