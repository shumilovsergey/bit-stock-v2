from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# users
class TelegramUsers(models.Model):
    ACCESS_LIST =[
        ('1', 'не подтвержденный'),
        ('2', 'подтвержденный'),
        ('3', 'админ')
    ]

    session_id = models.CharField("id сессии", max_length=56, unique=True)
    tg_id = models.CharField("телеграм id", max_length=56, default="no-auth")
    name = models.CharField("имя", max_length=56, default="no-auth")
    created = models.DateTimeField("создан", auto_now_add=True)
    access = models.CharField(max_length=1, choices=ACCESS_LIST, default=1)
    def __str__(self):
        return f"{self.tg_id} ~ {self.name} ~ {self.access}"
    class Meta:
        ordering = ['-created']
        verbose_name = "1. пользователь Телеграм"
        verbose_name_plural = "1. пользователи Телеграм"



class Shop(models.Model):
    name = models.CharField("название магазина", max_length=56, unique=True)
    created = models.DateTimeField("создан", auto_now_add=True)
    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
        if self.name == 'unsort':
            raise ValidationError("Нельзя удалять unsort")
        super().delete(*args, **kwargs)
    class Meta:
        ordering = ['-created']
        verbose_name = "3. магазин"
        verbose_name_plural = "3. магазины"



class UserCard(models.Model):
    tg_id = models.CharField("телеграм id", max_length=56)
    tg_add = models.CharField("телеграм адрес", max_length=56, default="empty")
    name = models.CharField("имя", max_length=56, default="empty")
    second_name = models.CharField("фамилия", max_length=56, default="empty")
    third_name =models.CharField("отчество", max_length=56, default="empty")
    shop = models.ForeignKey(Shop, on_delete=models.SET_DEFAULT, default=1)
    created = models.DateTimeField("дата регистрации", auto_now_add=True)
    valid = models.BooleanField("валидация", default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "2. карточка сотрудника"
        verbose_name_plural = "2. карточки сотрудников"
        ordering = ['-created']

# products
class Categories(models.Model):
    name = models.CharField("название категории", max_length=56, unique=True)
    created = models.DateTimeField("дата регистрации", auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']
        verbose_name = "4. категория"
        verbose_name_plural = "4. категории"

class Brands(models.Model):
    name = models.CharField("название бренда", max_length=56)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    created = models.DateTimeField("дата регистрации", auto_now_add=True)
    def __str__(self):
        return f"{self.category} ~ {self.name}"
    class Meta:
        ordering = ['-created']
        verbose_name = "5. бренд"
        verbose_name_plural = "5. бренды"

class Products(models.Model):
    name = models.CharField("название продукта", max_length=56)
    brand = models.ForeignKey(Brands, on_delete=models.PROTECT)
    amount = models.IntegerField("количество товара", default=0)
    created = models.DateTimeField("дата регистрации", auto_now_add=True)
    def __str__(self):
        return f"{self.brand} ~ {self.name}"
    class Meta:
        ordering = ['-created']
        verbose_name = "6. товар"
        verbose_name_plural = "6. товары"

# operations

# logs

