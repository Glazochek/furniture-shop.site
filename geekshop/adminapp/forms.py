import hashlib
import random
from django.db import models
from django import forms
from authapp.models import User
from authapp.forms import UserEditForm
from django.contrib.auth.forms import UserCreationForm
from mainapp.models import ProductCategory
from mainapp.models import Product


class UserAdminRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


class UserAdminEditForm(UserEditForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserAdminEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for filed_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-imput'


class ProductCategoryEditForm(forms.ModelForm):

    discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        # fields = '__all__'
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
