import hashlib
from random import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.forms import ClearableFileInput

from .models import User
from .models import UserProfile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['username'].required = True
        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

        # def clean_username(self):
        #     data = self.cleaned_data['username']
        #     if not data.isalpha():
        #         raise ValidationError('Имя пользователя не может содержать цифры')
        #      return data
        #


class UserRegisterForm(UserCreationForm):
    class Meta:

        model = User
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return data

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = True
        salt = hashlib.sha1(str(random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user


class UserEditForm(UserChangeForm):
    class Meta:

        model = User
        fields = ('image', 'username', 'first_name', 'email', 'age', 'password')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget = forms.ClearableFileInput()
                field.widget.attrs['class'] = 'img-edit form-control'
            elif field_name == 'username':
                field.widget.attrs['class'] = 'username-edit form-control'
                field.widget.attrs['placeholder'] = 'username'
            elif field_name == 'first_name':
                field.widget.attrs['class'] = 'first_name-edit form-control'
                field.widget.attrs['placeholder'] = 'name'
            elif field_name == 'email':
                field.widget.attrs['class'] = 'email-edit form-control'
                field.widget.attrs['placeholder'] = 'email'
            elif field_name == 'age':
                field.widget.attrs['class'] = 'age-edit form-control'
                field.widget.attrs['placeholder'] = 'age'
            elif field_name == 'password':
                field.widget.attrs['class'] = 'edit-password form-control'
                field.widget.attrs['placeholder'] = 'password'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('tagline', 'gender', 'aboutMe')

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            if field_name == 'tagline':
                field.widget.attrs['class'] = 'tagline-edit form-control'
                field.widget.attrs['placeholder'] = 'теги'
            elif field_name == 'gender':
                field.widget.attrs['class'] = 'gender-edit form-control'
                field.widget.attrs['placeholder'] = 'пол'
            elif field_name == 'aboutMe':
                field.widget.attrs['class'] = 'aboutMe-edit form-control'
                field.widget.attrs['placeholder'] = 'о себе'
