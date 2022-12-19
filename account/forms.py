from django import forms
from django.contrib.auth.models import User
from shop.models import Customer

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def validate(self):
        if self.username < 11 or self.username > 11:
            raise forms.ValidationError('Phone Number must have 11 digits')

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'district', 'city', 'address']