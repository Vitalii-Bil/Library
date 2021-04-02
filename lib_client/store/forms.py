from django import forms
from django.core.exceptions import ValidationError

from .models import CartItem


class OrderForm(forms.Form):
    email = forms.EmailField(required=True, max_length=254)
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', help_text='Example: +380969999999')
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)


class CartItemForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ['quantity']

    def clean_quantity(self):
    	data = self.cleaned_data['quantity']
    	if data > self.instance.book.quantity:
    		raise ValidationError(f'We have in stock only {self.instance.book.quantity} books. Choose a smaller quantity')
    	return data
