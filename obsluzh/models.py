from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class MyUser(models.Model):

    WHO = (
        ('Производитель', "Производитель"),
        ('Поставщик', "Поставщик"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, verbose_name="Логотип")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Номер телефона")
    email = models.EmailField(max_length=255, verbose_name="Электронная почта")
    obl = models.CharField(max_length=255, verbose_name='Ваш регион')
    who = models.CharField(max_length=255, choices=WHO, default='Поставщик', verbose_name='Статус пользователя')

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование категории продуктов')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Ptoduct(models.Model):
    WHO = (
        ('Производитель', "Производитель"),
        ('Поставщик', "Поставщик"),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    parent = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Наименование продукта')
    photo = models.ImageField(upload_to='product/', verbose_name='Фотография продукта')
    info = models.TextField(verbose_name='Описание услуги')
    status = models.CharField(max_length=255, choices=WHO, default='Производитель', verbose_name='От кого')
    reg = models.CharField(max_length=255, verbose_name='Регион')
    start_price = models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена на услугу')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class PriceList(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Ptoduct)

    class Meta:
        verbose_name = 'Прайс-лист'
        verbose_name_plural = 'Прайс-листы'

    def __str__(self):
        return f'Прайс-лист {self.owner}'


class OrderList(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    orders = models.ManyToManyField('Order')

    class Meta:
        verbose_name = 'Лист заказов'
        verbose_name_plural = 'Листы заказов'

    def __str__(self):
        return f'Лист заказов {self.owner}'

class Order(models.Model):
    product = models.ForeignKey(Ptoduct, on_delete=models.CASCADE)
    fio = models.CharField(max_length=255, null=True, verbose_name="ФИО")
    phone_number = models.CharField(max_length=18, verbose_name="Номер телефона:")
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Предлагаемая цена")
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name="Комментарий:")
    status = models.IntegerField(verbose_name='Количество просмотров')
    to_user = models.ForeignKey(MyUser, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(MyUser, related_name='from_user', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ {self.fio}"


