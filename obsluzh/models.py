from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class MyUser(models.Model):

    WHO = (
        ('Покупатель', "Покупатель"),
        ('Продавец', "Продавец"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, verbose_name="Логотип")
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="Номер телефона")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Электронная почта")
    price_password = models.CharField(max_length=255, null=True, blank=True, verbose_name="Пароль для прайс-листа")
    who = models.CharField(max_length=255, choices=WHO, default='Покупатель', verbose_name='Статус пользователя')

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Наименование продукта')
    start_price = models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена на продукт')
    opt_price = models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Оптовая цена')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class PriceList(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

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
    STATUS = (
        ("Запланирован", "Запланирован"),
        ("Отменен", "Отменен"),
        ("Готов", "Готов")
    )
    fio = models.CharField(max_length=255, null=True, verbose_name="ФИО")
    phone_number = models.CharField(max_length=16, null=True, blank=True, verbose_name="Номер телефона:")
    address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Предварительная цена")
    status = models.CharField(max_length=255, choices=STATUS, default="Запланирован", verbose_name="статус")
    hour = models.CharField(max_length=2, verbose_name="Час")
    day = models.CharField(max_length=2, verbose_name="День")
    mounth = models.CharField(max_length=10, verbose_name="Месяц")
    year = models.CharField(max_length=4, verbose_name="Год")
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name="Комментарий:")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ {self.day} {self.mounth} {self.year} на {self.hour}:00 "


