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
    path('profile', profile, name='prof'),

    path('start', start, name='start'),
    path('main', main, name='main'),
    path('map', map, name='map'),
    path('lk', lk, name='lk'),

    # path('region', select_region, name='region'),
    path('region/', select_region, name='region'),


    path('price', price, name='price'),
    path('price/remove_<int:pk>', remove_product, name='remove product'),
    path('price/remove_category_<int:pk>', remove_category, name='remove category'),
    path('price/info_<int:pk>', price_info, name='info product'),
    path('price/reform_<int:pk>',reform_product, name='reform product'),
    path('price/reform_category_<int:pk>',reform_category, name='reform category'),
    path('price/add', add_product, name='add product'),
    path('price/add_category', add_category, name='add category'),



    path('catalog_<str:reg>_<str:who>', catalog, name='catalog'),
    path('info_product_<int:pk>', info_product, name='product_detail'),

    path('create_order<int:pk>', create_order, name='create order'),

    path('other_lk_<int:pk>', other_lk, name='other_lk')


]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)