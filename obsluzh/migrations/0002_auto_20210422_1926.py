# Generated by Django 3.2 on 2021-04-22 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsluzh', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='price_password',
        ),
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='Электронная почта'),
        ),
    ]
