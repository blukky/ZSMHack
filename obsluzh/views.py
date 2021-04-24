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


def get_order_list(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(user=request.user)
        price = OrderList.objects.filter(owner=user).first()
        if not price:
            price = OrderList.objects.create(owner=user)
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
            im.save(settings.MEDIA_ROOT + f"/load_{form.cleaned_data['username']}.png", 'PNG')
            user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            new_user = MyUser.objects.create(user=user)
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
            return redirect('main')
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

    conn = sqlite3.connect("SMZ.db")
    cursor = conn.cursor()

    sql = 'select "Широта" from "Состав самозанятых"'
    cursor.execute(sql)
    x = cursor.fetchall()

    sql = 'select "Долгота" from "Состав самозанятых"'
    cursor.execute(sql)
    y = cursor.fetchall()

    sql = 'select "Код" from "Состав самозанятых"'
    cursor.execute(sql)
    kod = cursor.fetchall()

    sql = 'select "Тип " from "Состав самозанятых"'
    cursor.execute(sql)
    name = cursor.fetchall()

    sql = 'select "Адрес" from "Состав самозанятых"'
    cursor.execute(sql)
    address = cursor.fetchall()

    sql = 'select "Руководитель" from "Состав самозанятых"'
    cursor.execute(sql)
    ruk = cursor.fetchall()

    sql = 'select "Наименование региона" from "Состав самозанятых"'
    cursor.execute(sql)
    region = cursor.fetchall()

    sql = 'select "Описание ОКВЭД" from "Состав самозанятых"'
    cursor.execute(sql)
    okved = cursor.fetchall()

    # 'SELECT "Код","Тип ","Адрес","Руководитель","Наименование региона","Описание ОКВЭД"  FROM "Состав самозанятых" WHERE "Широта"="54,45277778"'

    mass_x = list()
    mass_y = list()

    mass_kod = list()
    mass_name = list()
    mass_address = list()
    mass_ruk = list()
    mass_region = list()
    mass_okved = list()

    for i in range(len(x)):

        try:
            mass_x.append(float(x[i][0].replace(",", ".")))
            mass_y.append(float(y[i][0].replace(",", ".")))
            mass_kod.append(str(kod[i][0]))
            mass_name.append(str(name[i][0]))
            mass_address.append(str(address[i][0]))
            mass_ruk.append(str(ruk[i][0]))
            mass_region.append(str(region[i][0]))
            mass_okved.append(str(okved[i][0]))


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

    center_map = [64.32087158, 93.515625]
    map = folium.Map(location=center_map, zoom_start=3, tiles='Stamen Terrain')

    marker_cluster = MarkerCluster().add_to(map)

    tooltip = "Подробнее..."

    # def kachestvo():
    #     return np.random.choice(['Низкое', 'Среднее', 'Высокое'], 1)[0]

    # df = pd.DataFrame(columns=['a','b','c','d','e','f'], index=['x','y'])
    # df.loc['x'] = pd.Series({'a':'Наименование', 'b':'Адрес', 'c':'Руководитель', 'd':'Наименование региона', 'e':'ОКВЭД', 'f':'Описание ОКВЭД'})
    # df.loc['y'] = pd.Series({'a':mass_name, 'b':mass_ruk, 'c':mass_address, 'd':3, 'e':1, 'f':1})

    # 'SELECT "Код","Тип ","Адрес","Руководитель","Наименование региона","Описание ОКВЭД"  FROM "Состав самозанятых" WHERE "Широта"="54,45277778"'

    df = {'Код': [mass_kod], 'Наименование': [mass_name], 'Адрес': [mass_address], 'Руководитель': [mass_ruk],
          'Наименование региона': [mass_region], 'Описание ОКВЭД': [mass_okved]}
    df = pd.DataFrame.from_dict(df)

    print(df)

    df.to_html()

    import branca

    def fancy_html(row):
        # i = row
        # mass_name=df['Наименование'].iloc[i]
        # print("########################")
        # print(mass_name)

        html = """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Стили</title>
        <style type="text/css">
        table {
            font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
            text-align: center;
            border-collapse: collapse;
            border-spacing: 5px;
            background: #E1E3E0;
            border-radius: 20px;
            }
            th {
            font-size: 22px;
            font-weight: 300;
            padding: 12px 10px;
            border-bottom: 2px solid #F56433;
            color: #F56433;
            }
            tbody tr:nth-child(2) {
            border-bottom: 2px solid #F56433;
            }
            td {
            padding: 10px;
            color: #8D8173;
            }
        </style>
        </head>
        <body>
            <table>
                <tr><th colspan="6">Подробнее:</th></tr>
                <tr>
                <td>Наименование</td>
                <td>Адрес</td>
                <td>Руководитель</td>
                <td>Наименование региона</td>
                <td>ОКВЭД</td>
                <td>Описание ОКВЭД</td>
                </tr>
                <tr>
                <td>ООО "СВ ГЛАСС ИНДАСТРИ"</td>
                <td>601389, Владимирская обл, поселок Им Воровского, район Судогодский, улица Воровского, 10</td>
                <td>Власов Владимир Геннадьевич</td>
                <td>Владимирская область</td>
                <td>23,1</td>
                <td>Производство стекла и изделий из стекла</td>
                </tr>
            </table>
        </body>
        </html>
        """
        return html

    #     popup = """
    #                 <div align="center">
    #                     <br>
    #                     <iframe width="600" height="400" frameborder="0" scrolling="no"
    #                         {{ html|safe }}
    #                     </iframe></div>
    # """

    # <iframe src="https://www.youtube.com/embed/hvoD7ehZPcM?autoplay=1&amp;autohide=1" frameborder="0" allowfullscreen="" style="width="800" height="400""></iframe>

    #     popup = '\
    #                 <div align="center"> \
    #                     Подробная информация: <br>\
    #                     <iframe width="800" height="400" frameborder="0" scrolling="no" \
    #                         src="//plotly.com/~wqsfedvf/1.embed"> \
    #                     </iframe></div> \
    # '
    # iframe = branca.element.IFrame(html=html,width=800,height=250)

    for i in range(len(mass_name)):
        html = fancy_html(i)

        iframe = branca.element.IFrame(html=html, width=800, height=250)
        popup = folium.Popup(iframe, parse_html=True)

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

    context = {'map': map}
    conn.close()
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
    data = {'user': get_user(request), 'products': products, 'orders': orders}
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
    data = {'user': get_user(request), 'products': product, 'region': region, 'reg': reg, 'who': who, 'categories':categories}

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
            order = Order.objects.create(
                product=product,
                fio=form.cleaned_data['fio'],
                phone_number=form.cleaned_data['phone_number'],
                price=form.cleaned_data['price'],
                comment=form.cleaned_data['comment'],
                status=0,
                to_user=product.parent,
                from_user=get_user(request)
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
