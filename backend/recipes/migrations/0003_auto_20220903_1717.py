# Generated by Django 2.2.19 on 2022-09-03 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220902_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(help_text='Введите название ингредиента', max_length=100, verbose_name='Название ингредиента'),
        ),
    ]