from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def validate(self):
        if self.username < 11 or self.username > 11:
            raise forms.ValidationError('Phone Number must have 11 digits')