from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import *
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User
from .forms import *
from django.forms.models import model_to_dict
from django.contrib.auth import login, logout, authenticate
from django.core.mail import EmailMessage, send_mail
import datetime
import locale
import re
import pdfkit
from django.http import HttpResponseNotFound, JsonResponse

def get_user(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(user=request.user)
    else:
        user = ''
    return user

def index(request):
    user = get_user(request)
    data = {'user': user}
    return render(request, 'base.html', data)

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
        else:
            return render(request, "login.html", {'form': form, 'user': get_user(request)})
    else:
        form = UserLoginForm()
    return render(request, "login.html", {'form': form, 'user': get_user(request)})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            im = Image.open(BytesIO(form.cleaned_data['avatar'].read()))
            im.save(settings.MEDIA_ROOT+f"/load_{form.cleaned_data['username']}.jpg", 'JPEG')
            user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.save()
            new_user = MyUser.objects.create(user=user)
            new_user.email = form.cleaned_data['email']
            new_user.avatar = settings.MEDIA_ROOT+f"/load_{form.cleaned_data['username']}.jpg"
            new_user.phone = form.cleaned_data['phone']
            new_user.who = form.cleaned_data['who']
            new_user.save()
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            return redirect('main')
        else:
            data = {'form': form, 'user': get_user(request)}
            return render(request, 'register.html', data)
    else:
        form = UserRegisterForm()
        data = {'form':form, 'user':get_user(request)}
        return render(request, 'register.html', data)

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def main(request):
    return render(request, 'base.html')

def profile(request):
    return render(request, 'base.html')

def price(request):
    return render(request, 'base.html')

def remove_product(request):
    return render(request, 'base.html')

def reform_product(request):
    return render(request, 'base.html')

def add_product(request):
    return render(request, 'base.html')


