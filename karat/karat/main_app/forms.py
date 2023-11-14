# from django.forms import ModelForm
# from .models import Product, categories

# class ProductForm(ModelForm):
#   class Meta: 
#     model = Product
#     fields =  ['name','price', 'karat', 'category', 'weight', 'quantity_available', 'image']

#     category= forms.ModelChoiceField()


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')




    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )


USER_TYPE_CHOICES = (('A', 'Admin'),
('S', 'Seller'),
('C', 'Customer'),
)

class AddUser(UserCreationForm):

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')




    class Meta:
        model = User
        fields = ('user_type' ,'username', 'first_name', 'last_name', 'email', 'password1', 'password2' )




