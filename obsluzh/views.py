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
import tensorflow as tf
import random
from .wallet_one import *
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


def get_order_list(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(user=request.user)
        price = OrderList.objects.filter(owner=user).first()
        if not price:
            price = OrderList.objects.create(owner=user)
        return price


def index(request):
    user = get_user(request)
    df = pd.read_excel('Спрос.xlsx')
    df = np.array(df['Объём'])
    arr = df[-10:]
    print(arr)
    model = tf.keras.models.load_model('спрос_gru.h5')
    arr = np.expand_dims(arr, axis=0)
    arr = np.expand_dims(arr, axis=2)
    pred = model.predict(arr)[0][0]
    arr = np.append(arr, pred)
    spros = enumerate(arr)
    data = {'user': user, 'spros': spros}
    return render(request, 'base.html', data)


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
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
            im.save(settings.MEDIA_ROOT + f"/load_{form.cleaned_data['username']}.png", 'PNG')
            user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            new_user = MyUser.objects.create(user=user)
            token = get_token()
            extern = register_user(token)
            new_user.externalId = extern
            new_user.bind_uuid = add_samzan(extern, token)
            new_user.email = form.cleaned_data['email']
            new_user.avatar = settings.MEDIA_ROOT + f"/load_{form.cleaned_data['username']}.png"
            new_user.obl = form.cleaned_data['obl']
            new_user.phone = form.cleaned_data['phone']
            new_user.who = form.cleaned_data['who']
            new_user.save()
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            return redirect('home')
        else:
            data = {'form': form, 'user': get_user(request)}
            return render(request, 'register.html', data)
    else:
        form = UserRegisterForm()
        data = {'form': form, 'user': get_user(request)}
        return render(request, 'register.html', data)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


def map(request):
    #######################################################################################################

    import json
    with open("Sostav_SMZ.json", "r", encoding="utf8") as read_file:
        data = json.load(read_file)

    mass_x = list()
    mass_y = list()

    mass_kod = list()
    mass_name = list()
    mass_address = list()
    mass_ruk = list()
    mass_region = list()
    mass_okved = list()

    for i in range(len(data)):
        try:
            mass_x.append(float(data[i]["Широта"].replace(",", ".")))
            mass_y.append(float(data[i]["Долгота"].replace(",", ".")))

            mass_kod.append(str(data[i]["Код"]))
            mass_name.append(str(data[i]["Тип "]))
            mass_address.append(str(data[i]["Адрес"]))
            mass_ruk.append(str(data[i]["Руководитель"]))
            mass_region.append(str(data[i]["Наименование региона"]))
            mass_okved.append(str(data[i]["Описание ОКВЭД"]))

        except:
            pass

    def color_change(elev):
        if (elev < 2):
            return ('green')
        elif (1000 <= elev < 7):
            return ('orange')
        else:
            return ('red')

    center_map = [64.32087158, 93.515625]
    map = folium.Map(location=center_map, zoom_start=3, tiles='Stamen Terrain')

    marker_cluster = MarkerCluster().add_to(map)

    tooltip = "Подробнее..."

    # def kachestvo():
    #     return np.random.choice(['Низкое', 'Среднее', 'Высокое'], 1)[0]

    import branca

    def fancy_html(row):
        i = row
        # Date = df['Date'].iloc[i]

        # mass_kod[i]
        # mass_name[i]
        # mass_address[i]
        # mass_ruk[i]
        # mass_region[i]
        # mass_okved[i]

        html = """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Стили</title>
        <style type="text/css">
        table {{
            font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
            text-align: center;
            border-collapse: collapse;
            border-spacing: 5px;
            background: #E1E3E0;
            border-radius: 20px;
            }}
            th {{
            font-size: 22px;
            font-weight: 300;
            padding: 12px 10px;
            border-bottom: 2px solid #F56433;
            color: #F56433;
            }}
            tbody tr:nth-child(2) {{
            border-bottom: 2px solid #F56433;
            }}
            td {{
            padding: 10px;
            color: #8D8173;
            }}
        </style>
        </head>
        <body>
            <table>
                <tr><th colspan="6">Подробнее:</th></tr>
                <tr>
                <td>Поставщик</td>
                <td>Наименование</td>
                <td>Адрес</td>
                <td>Руководитель</td>
                <td>Наименование региона</td>
                <td>Описание ОКВЭД</td>
                </tr>
                <tr>
                <td>{}</td>""".format(mass_kod[i]) + """
                <td>{}</td>""".format(mass_name[i]) + """
                <td>{}</td>""".format(mass_address[i]) + """
                <td>{}</td>""".format(mass_ruk[i]) + """
                <td>{}</td>""".format(mass_region[i]) + """
                <td>{}</td>""".format(mass_okved[i]) + """
                </tr>
            </table>
        </body>
        </html>
        """
        return html

    for i in range(len(mass_name)):
        html = fancy_html(i)

        iframe = branca.element.IFrame(html=html, width=1000, height=250)
        popup = folium.Popup(iframe, parse_html=True)

        folium.Marker(location=[mass_x[i], mass_y[i]],
                      popup=popup,
                      tooltip=tooltip,
                      icon=folium.Icon(color="darkred", icon="glyphicon glyphicon-home"),  # color="blue"
                      ).add_to(marker_cluster)

    html_string = map.get_root().render()

    map = map._repr_html_()

    context = {'map': map, 'user': get_user(request)}
    return render(request, 'map.html', context)


#######################################################################################################

def main(request):
    data = {'user': get_user(request)}
    return render(request, 'base.html', data)


def start(request):
    df = pd.read_csv('regions.csv')
    region = np.array(df['Облать'])
    df = pd.read_csv('Поселок.csv')
    pos = np.array(df['Поселок'])
    data = {'region': region, 'user': get_user(request), 'pos': pos}
    return render(request, 'start.html', data)


def lk(request):
    products = Ptoduct.objects.filter(parent=get_user(request))[:3]
    orders = Order.objects.filter(from_user=get_user(request))[:3]
    df = pd.read_excel('Предложение.xlsx')
    df = np.array(df['Объём'])
    arr = df[-10:]
    model = tf.keras.models.load_model('предложение_gru.h5')
    arr = np.expand_dims(arr, axis=0)
    arr = np.expand_dims(arr, axis=2)
    pred = model.predict(arr)[0][4]
    arr = np.append(arr, pred)
    predlozh = enumerate(arr)
    data = {'user': get_user(request), 'products': products, 'orders': orders, 'predlozh': predlozh}
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
            product.parent = user
            product.name = form.cleaned_data['name']
            product.photo = path
            product.info = form.cleaned_data['info']
            product.reg = user.obl
            product.status = 'Производитель' if user.who == 'Поставщик' else 'Поставщик'
            product.start_price = form.cleaned_data['start_price']
            product.save()
            return redirect('price')
        else:
            product = Ptoduct.objects.get(pk=pk)
            categories = Category.objects.all()
            data = {'user': get_user(request), 'categories': categories, 'form': form, 'product': product}
            return render(request, 'reform_product.html', data)
    else:
        product = Ptoduct.objects.get(pk=pk)
        categories = Category.objects.all()
        form = ProductForm(initial=model_to_dict(product))
        data = {'user': get_user(request), 'form': form, 'categories': categories, 'product': product}
    return render(request, 'reform_product.html', data)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():

            user = get_user(request)
            path = settings.MEDIA_ROOT + f"/product/{form.cleaned_data['name']}.jpg"
            im = Image.open(BytesIO(form.cleaned_data['photo'].read()))
            im.save(path, 'JPEG')
            poduct = Ptoduct.objects.create(parent=user,
                                            category=form.cleaned_data['category'],
                                            name=form.cleaned_data['name'],
                                            photo=path,
                                            info=form.cleaned_data['info'],
                                            reg=user.obl,
                                            status='Производитель' if user.who == 'Поставщик' else 'Поставщик',
                                            start_price=form.cleaned_data['start_price']
                                            )
            poduct.save()
            price_list = get_price(request)
            price_list.products.add(poduct)
            price_list.save()
            return redirect('price')
        else:
            categories = Category.objects.all()
            data = {'user': get_user(request), 'form': form, 'categories': categories}
            return render(request, 'add_product.html', data)
    else:
        form = ProductForm()
        categories = Category.objects.all()
        data = {'user': get_user(request), 'form': form, 'categories': categories}
        return render(request, 'add_product.html', data)


def price(request):
    price_list = get_price(request)
    product = price_list.products.all()
    data = {'user': get_user(request), 'products': product}
    return render(request, 'price-list.html', data)


def price_info(request, pk):
    product = Ptoduct.objects.get(pk=pk)
    data = {'user': get_user(request), 'product': product}
    return render(request, 'product_detail.html', data)


#####################################

def catalog(request, reg, who):
    reg = reg.replace('_', " ")
    df = pd.read_csv('regions.csv')
    region = np.array(df['Облать'])
    product = Ptoduct.objects.all()
    categories = Category.objects.all()
    data = {'user': get_user(request), 'products': product, 'region': region, 'reg': reg, 'who': who,
            'categories': categories}

    return render(request, 'catalog.html', data)


def other_lk(request, pk):
    other_user = MyUser.objects.get(pk=pk)
    products = Ptoduct.objects.filter(parent=other_user)
    count_order_to = len(Order.objects.filter(to_user=other_user))
    count_order_from = len(Order.objects.filter(from_user=other_user))
    count = [count_order_to, count_order_from]
    data = {'user': get_user(request), 'other_user': other_user, 'products': products, 'count': count}
    return render(request, 'other_lk.html', data)


def info_product(request, pk):
    product = Ptoduct.objects.get(pk=pk)
    data = {'user': get_user(request), 'product': product}
    return render(request, 'info_product.html', data)


def create_order(request, pk):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product = Ptoduct.objects.get(pk=pk)
            token = get_token()
            user = get_user(request)
            order = Order.objects.create(
                product=product,
                fio=form.cleaned_data['fio'],
                phone_number=form.cleaned_data['phone_number'],
                price=form.cleaned_data['price'],
                comment=form.cleaned_data['comment'],
                status=0,
                to_user=product.parent,
                from_user=user,
                invoiceid=create_invoice(user.externalId, str(form.cleaned_data['price']))
            )
            order.save()
            orderlist = get_order_list(request)
            orderlist.orders.add(order)
            orderlist.save()
            return redirect('my order')
        else:
            data = {'user': get_user(request), 'form': form}
            return render(request, 'create_order.html', data)
    else:
        form = OrderForm()
        data = {'user': get_user(request), 'form': form}
        return render(request, 'create_order.html', data)


def my_order(request):
    orders = Order.objects.filter(from_user=get_user(request))
    data = {'orders': orders, 'user': get_user(request), 'title': "Мои заказы"}
    return render(request, 'my_order.html', data)


def my_predlozh(request):
    orders = Order.objects.filter(to_user=get_user(request))
    data = {'orders': orders, 'user': get_user(request), 'title': "Мои предложения"}
    return render(request, 'my_order.html', data)


def info_order(request, pk):
    order = Order.objects.get(pk=pk)
    data = {'user': get_user(request), 'order': order}
    return render(request, 'info_order.html', data)


######################## AJAX

def select_region(request):
    print(request.POST)
    if request.method == 'POST':
        data = dict()
        df = pd.read_csv('Поселок.csv')
        pos = np.array(df[df['Область'] == request.POST['region']]['Поселок'])
        for i in range(len(pos)):
            data[i] = pos[i]
        return JsonResponse(data)
