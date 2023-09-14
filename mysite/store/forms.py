from django import forms
from .models import Laptop, Image, Brand
from account.models import User
import re

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['name', 'brand', 'graphic_card',
                  'ram', 'cpu', 'screen_type', 'price']

    def clean_ram(self):
        ram = self.cleaned_data.get('ram')
        if not isinstance(ram, int):
            raise forms.ValidationError("RAM must be an integer")
        return ram

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price


class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Image
        fields = ['description', 'image', 'laptop']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'info', 'headquarters','phone', 'email']

    def val_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, phone):
            raise forms.ValidationError("Invalid phone number")
        return phone


class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control ",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    ROLES= [
    ('Customer', 'Customer'),
    ('Admin', 'Admin'),
    ]
    role= forms.CharField(
        # initial=self.cleaned_data.get('is_customer')
        label='Role', 
        widget=forms.RadioSelect(choices=ROLES),
    )
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'role')
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('role') == 'Admin':
            user.is_superuser = True
            user.is_customer = False
        else:
            user.is_superuser = False
            user.is_customer = True

        if commit:
            user.save()
        return user
