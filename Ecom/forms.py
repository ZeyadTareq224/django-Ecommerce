from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
	('S', 'Stripe'),
	('P', 'PayPal'),
	)
class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder': '1234 Main St'
		}))

    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
		'class': 'custom-select d-block w-100'
		}))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'City'
    }))

    zipcode = forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control'
		}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

