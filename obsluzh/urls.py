from . import views
from .views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='home'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('register', register, name='reg'),

    path('start', start, name='start'),
    path('main', main, name='main'),
    path('map', map, name='map'),
    path('lk', lk, name='lk'),
    path('support', support, name='support'),

    # path('region', select_region, name='region'),
    path('region/', select_region, name='region'),


    path('price', price, name='price'),
    path('price/remove_<int:pk>', remove_product, name='remove product'),
    path('price/info_<int:pk>', price_info, name='info product'),
    path('price/reform_<int:pk>',reform_product, name='reform product'),
    path('price/add', add_product, name='add product'),



    path('catalog_<str:reg>_<str:who>', catalog, name='catalog'),
    path('info_product_<int:pk>', info_product, name='product_detail'),

    path('create_order<int:pk>', create_order, name='create order'),


    path('my_order', my_order, name='my order'),
    path('my_predlozh', my_predlozh, name='my predlozh'),


    path('info_order_<int:pk>', info_order, name='info order'),



    path('other_lk_<int:pk>', other_lk, name='other_lk')


]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)