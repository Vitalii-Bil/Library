from django import forms

from phonenumber_field.modelfields import PhoneNumberField

from .models import Cart


class OrderForm(forms.Form):
    email = forms.EmailField(required=True, max_length=254)
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', help_text='Example: +380969999999')
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
