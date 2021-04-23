from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import *


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ('avatar', 'email', 'phone', 'obl', 'who')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'obl': forms.TextInput(attrs={'class': 'form-control'}),
            'who': forms.Select(attrs={'class': 'form-control'})
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'margin: 10px 0; color: #7F7F7F'}))
    password = forms.CharField(label='Пароль:',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'style': 'margin: 10px 0; color: #7F7F7F'}))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Ptoduct
        fields = ('name', 'category', 'photo', 'info', 'start_price')
