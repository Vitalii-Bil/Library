from django import forms

from phonenumber_field.modelfields import PhoneNumberField

from .models import Cart


class OrderForm(forms.Form):
    email = forms.EmailField()
    phone = PhoneNumberField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
