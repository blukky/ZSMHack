from . import views
from .views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='home'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', register, name='reg'),
    path('profile', profile, name='prof'),


    path('price', price, name='price'),
    path('price/remove_<int:pk>', remove_product, name='remove product'),
    path('price/reform_<int:pk>',reform_product, name='reform product'),
    path('price/add', add_product, name='add product'),


]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)