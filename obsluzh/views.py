from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import *
from .forms import *
from django.forms.models import model_to_dict
from django.contrib.auth import login, logout
from django.core.mail import EmailMessage, send_mail
import datetime
import locale
import re
import pdfkit
from django.http import HttpResponseNotFound, JsonResponse


def index(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'base.html')

def register(request):
    return render(request, 'base.html')

def logout(request):
    return render(request, 'base.html')

def profile(request):
    return render(request, 'base.html')

def start(request):
    return render(request, 'start.html')

def price(request):
    return render(request, 'base.html')

def remove_product(request):
    return render(request, 'base.html')

def reform_product(request):
    return render(request, 'base.html')

def add_product(request):
    return render(request, 'base.html')


