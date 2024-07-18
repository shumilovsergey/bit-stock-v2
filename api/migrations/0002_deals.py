# Generated by Django 5.0.6 on 2024-07-18 13:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('tg_id', models.CharField(max_length=56, verbose_name='телеграм id')),
                ('tg_add', models.CharField(max_length=56, verbose_name='телеграм add')),
                ('user_name', models.CharField(max_length=56, verbose_name='имя сотрудника')),
                ('category', models.CharField(max_length=56, verbose_name='категория')),
                ('brand', models.CharField(max_length=56, verbose_name='бренд')),
                ('product', models.CharField(max_length=56, verbose_name='продукт')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество')),
                ('prise', models.IntegerField(verbose_name='цена за штуку')),
                ('tota_prise', models.IntegerField(verbose_name='итоговая цена')),
                ('type', models.CharField(choices=[('1', '+'), ('2', '-')], max_length=1, verbose_name='доход // расход')),
            ],
            options={
                'verbose_name': '7. сделка',
                'verbose_name_plural': '7. сделки',
                'ordering': ['-created'],
            },
        ),
    ]
