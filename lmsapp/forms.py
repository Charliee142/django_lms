from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from lmsapp.models import *


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}))
    last_name =  forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Your Email'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'City'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zip'}))
    street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apartment or Suite'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'state'}))
    country = CountryField(blank_label='Please Select a Valid Country').formfield(required=False, widget=CountrySelectWidget(attrs={
            'class': 'form-select',
        }))


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Review Title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Review Content'}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }