from django import forms

from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'address1', 'address2', 'city', 'state', 'zipcode']
        exclude = ['user']
        labels = {
            'full_name': 'Full Name',
            'email': 'Email',
            'address1': 'Address Line 1',
            'address2': 'Address Line 2',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zip Code',
        }
