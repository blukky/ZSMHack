from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import *
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User
from .forms import *
import folium
import requests as r
from bs4 import BeautifulSoup as bs
import folium
from folium.plugins import MarkerCluster
from folium import IFrame
import sqlite3
from .models import *
import random
import numpy as np
from django.forms.models import model_to_dict
from django.contrib.auth import login, logout, authenticate
from django.core.mail import EmailMessage, send_mail
import datetime
import pandas as pd
import numpy as np
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

def get_price(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(user=request.user)
        price = PriceList.objects.filter(owner=user).first()
        if not price:
            price = PriceList.objects.create(owner=user)
        return price

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
            new_user.obl = form.cleaned_data['obl']
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
    return redirect('start')


def map(request):
    #######################################################################################################

    conn = sqlite3.connect("db_smz.file")
    cursor = conn.cursor()

    sql = 'select "Широта" from "Состав самозанятых"'
    cursor.execute(sql)
    x = cursor.fetchall()

    sql = 'select "Долгота" from "Состав самозанятых"'
    cursor.execute(sql)
    y = cursor.fetchall()

    sql = 'select "Дата регистрации" from "Состав самозанятых"'
    cursor.execute(sql)
    name = cursor.fetchall()

    sql = 'select "Руководитель" from "Состав самозанятых"'
    cursor.execute(sql)
    ruk = cursor.fetchall()

    sql = 'select "Адрес" from "Состав самозанятых"'
    cursor.execute(sql)
    address = cursor.fetchall()

    # 'SELECT "Код","Тип ","Адрес","Руководитель","Наименование региона","Описание ОКВЭД"  FROM "Состав самозанятых" WHERE "Широта"="54,45277778"'

    mass_x = list()
    mass_y = list()
    mass_name = list()
    mass_ruk = list()
    mass_address = list()

    for i in range(len(x)):

        try:
            mass_x.append(float(x[i][0].replace(",", ".")))
            mass_y.append(float(y[i][0].replace(",", ".")))
            mass_name.append(str(name[i][0]))
            mass_ruk.append(str(ruk[i][0]))
            mass_address.append(str(address[i][0]))


        except:
            pass

    # print(mass_address)

    def color_change(elev):
        if (elev < 2):
            return ('green')
        elif (1000 <= elev < 7):
            return ('orange')
        else:
            return ('red')

    map = folium.Map(location=[64.32087158, 93.515625], zoom_start=3, tiles='Stamen Terrain')

    marker_cluster = MarkerCluster().add_to(map)

    tooltip = "Подробнее..."
    # def kachestvo():
    #     return np.random.choice(['Низкое', 'Среднее', 'Высокое'], 1)[0]

    html = """
    <h1> This is a big popup</h1><br>
    With a few lines of code...
    <p>
    <code>
        from numpy import *<br>
        exp(-2*pi)
    </code>
    </p>
    """
    # iframe = folium.Element.IFrame(html=html, width=500, height=300)
    # popup = folium.Popup(iframe, max_width=2650)
    popup = '\
                <div align="center"> \
                    HTML <br>\
                    <iframe width="800" height="400" frameborder="0" scrolling="no" \
                        src="//plotly.com/~wqsfedvf/1.embed"> \
                    </iframe></div> \
'

    for i in range(len(mass_name)):
        folium.Marker(location=[mass_x[i], mass_y[i]],
                      popup=popup,

                      # popup=f"Наименование: {mass_name[i]}\n\n \
                      #         Руководитель: {mass_ruk[i]}\n\n \
                      #         Адрес: {mass_address[i]}\n\n \

                      #             ",  

                      tooltip=tooltip,
                      icon=folium.Icon(color="darkred", icon="glyphicon glyphicon-home"),  # color="blue"
                      ).add_to(marker_cluster)

    html_string = map.get_root().render()

    map = map._repr_html_()

    context = {'map': map, 'user': get_user(request)}
    conn.close()
    return render(request, 'map.html', context)


#######################################################################################################

def main(request):
    data = {'user': get_user(request)}
    return render(request, 'base.html')

def profile(request):
    return render(request, 'base.html')

def start(request):
    df = pd.read_csv('regions.csv')
    region = np.array(df['Облать'])
    df = pd.read_csv('Поселок.csv')
    pos = np.array(df['Поселок'])
    data = {'region': region, 'user':get_user(request), 'pos':pos}
    return render(request, 'start.html', data)

    
def lk(request):
    data = {'user': get_user(request)}
    return render(request, 'lk.html', data)

####################################
# Лист услуг
####################################
def remove_product(request, pk):
    price_list = get_price(request)
    product = Ptoduct.objects.get(pk=pk)
    price_list.products.remove(product)
    product.delete()
    price_list.save()
    return redirect('price')

def reform_product(request, pk):
    if request.method == 'POST':
        product = Ptoduct.objects.get(pk=pk)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_user(request)
            path = settings.MEDIA_ROOT + f"/product/{form.cleaned_data['name']}.jpg"
            im = Image.open(BytesIO(form.cleaned_data['photo'].read()))
            im.save(path, 'JPEG')
            product.category = form.cleaned_data['category']
            product.parent = user.pk
            product.name = form.cleaned_data['name']
            product.photo = path
            product.info = form.cleaned_data['info']
            product.reg = user.obl
            product.status = 'Производитель' if user.who == 'Поставщик' else 'Поставщик'
            product.start_price = form.cleaned_data['start_price']
            product.save()
            return redirect('price')
        else:
            data = {'user': get_user(request), 'form': form}
            return render(request, 'reform_product.html', data)
    else:
        product = Ptoduct.objects.get(pk=pk)
        form = ProductForm(initial=model_to_dict(product))
        data = {'user': get_user(request), 'form': form}
    return render(request, 'reform_product.html', data)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():

            user = get_user(request)
            path = settings.MEDIA_ROOT + f"\\product\\{form.cleaned_data['name']}.jpg"
            im = Image.open(BytesIO(form.cleaned_data['photo'].read()))
            im.save(path, 'JPEG')
            poduct = Ptoduct.objects.create(parent=user.id,
                                   category=form.cleaned_data['category'],
                                   name=form.cleaned_data['name'],
                                   photo=path,
                                   info=form.cleaned_data['info'],
                                   reg=user.obl,
                                   status='Производитель' if user.who =='Поставщик' else 'Поставщик',
                                   start_price=form.cleaned_data['start_price']
                                   )
            poduct.save()
            price_list = get_price(request)
            price_list.products.add(poduct)
            price_list.save()
            return redirect('price')
        else:
            data = {'user': get_user(request), 'form': form}
            return render(request, 'add_product.html', data)
    else:
        form = ProductForm()
        data = {'user': get_user(request), 'form': form}
        return render(request, 'add_product.html', data)


def price(request):
    price_list = get_price(request)
    product = price_list.products.all()
    data = {'user':get_user(request), 'products':product}
    return render(request, 'price-list.html', data)

def price_info(request, pk):
    product = Ptoduct.objects.get(pk=pk)
    data = {'user': get_user(request), 'product': product}
    return render(request, 'product_detail.html', data)

#####################################

def catalog(request, reg, who):
    reg = reg.replace('_', " ")
    product = Ptoduct.objects.filter(status=who, reg=reg)

    data = {'user': get_user(request), 'products': product}

    return render(request, 'catalog.html', data)


def other_lk(request, pk):
    other_user = MyUser.objects.get(pk=pk)


    data = {'user': get_user(request),' other_user': other_user}

    return render(request, 'other_lk.html', data)

def info_product(request, pk):
    product = Ptoduct.objects.get(pk=pk)
    avtor = MyUser.objects.get(pk=product.parent)
    data = {'user': get_user(request), 'product': product, 'avtor':avtor}
    return render(request, 'info_product.html', data)

def create_order(request, pk):

    data = {}
    return render(request, 'create_order.html', data)

def my_order(request):
    return render(request, '')

def my_predlozh(request):
    return render(request)











######################## AJAX

def select_region(request):
    print(request.POST)
    if request.method == 'POST':
        data = dict()
        df = pd.read_csv('Поселок.csv')
        pos = np.array(df[df['Область']==request.POST['region']]['Поселок'])
        for i in range(len(pos)):
            data[i] = pos[i]
        return JsonResponse(data)


