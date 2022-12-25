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

    class Meta:
        ordering = ['created_at']
        
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
    
    class Meta:
        ordering = ['added_at']

    @property
    def discount(self):
        return self.regular_price - self.discount_price
    
    @property
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

    class Meta:
        ordering = ['added_at']

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
    total_amount = models.PositiveIntegerField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    pay_method = models.CharField(max_length=10, choices=utails.PAY_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=10, choices=utails.ORDER_STATUS, default=utails.ORDER_STATUS[0][0])
    will_arrive_on = models.DateField(null=True, blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordered_at']

    @property
    def is_deliverd(self):
        return True if self.status == 'deliverd' else False

    def save(self,*args,**kwargs):
        if not self.total_amount:
            self.total_amount = self.quantity * self.product.discount_price
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.product.title

class Payment(models.Model):
    _user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    _customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    orders = models.ManyToManyField(OrderPlaced)
    method = models.CharField(max_length=10, choices=utails.PAY_CHOICES, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0 , null=True, blank=True)
    paid = models.PositiveIntegerField(default=0, null=True, blank=True)
    due = models.PositiveIntegerField(default=0, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    tr_id = models.CharField(max_length=50, null=True, blank=True)
    approved = models.BooleanField(default=False, null=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['paid_at']

    def save(self,*args,**kwargs):
        self.due = self.amount - self.paid

        # update all Orderplaced model status to accepted
        # which is approved=true in Payment and is_paid=True in OrderPlaced
        try:
            if self.approved:
                user = self._user
                cus = self._customer
                pay_meth = self.method
                
                if user and cus:
                    prods_ids = [prod.product_id for prod in self.orders.all()]
                    order_placed_and_paid = OrderPlaced.objects.filter(
                        _user=user, _customer=cus, product__product_id__in=prods_ids,
                        pay_method=pay_meth, is_paid=True, status=utails.ORDER_STATUS[0][0] ) # ORDER_STATUS[0][0] = 'pending'

                    if order_placed_and_paid:
                        for order in order_placed_and_paid:
                            order.status =  utails.ORDER_STATUS[1][0] # ORDER_STATUS[1][0] = 'accepted'
                            order.save()
                    else:
                        print('placed order empty')
                else:
                    print('user or cus not valid')
            else:
                print(':: self not appreved')
        except Exception as e:
            print(e)
            raise Exception(e)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.method
