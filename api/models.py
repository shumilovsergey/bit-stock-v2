from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class TelegramUsers(models.Model):
    session_id = models.CharField("id сессии", max_length=56, unique=True)
    tg_id = models.CharField("телеграм id", max_length=56, default="no-auth")
    name = models.CharField("имя", max_length=56, default="no-auth")
    created = models.DateTimeField("создан", auto_now_add=True)
    valid = models.BooleanField("валидация", default=False)
    def __str__(self):
        return self.tg_id
    class Meta:
        ordering = ['-created']
        verbose_name = "пользователь Телеграм"
        verbose_name_plural = "пользователи Телеграм"

class Position(models.Model):
    name = models.CharField("Название магазина", max_length=56, unique=True)
    created = models.DateTimeField("создан", auto_now_add=True)
    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
        if self.name == 'unsort':
            raise ValidationError("Нельзя удалять unsort")
        super().delete(*args, **kwargs)
    class Meta:
        ordering = ['-created']
        verbose_name = "должность"
        verbose_name_plural = "должности"

class Shop(models.Model):
    name = models.CharField("Название магазина", max_length=56, unique=True)
    created = models.DateTimeField("создан", auto_now_add=True)
    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
        if self.name == 'unsort':
            raise ValidationError("Нельзя удалять unsort")
        super().delete(*args, **kwargs)
    class Meta:
        ordering = ['-created']
        verbose_name = "магазин"
        verbose_name_plural = "магазины"

class UserCard(models.Model):
    tg_id = models.CharField("телеграм id", max_length=56)
    tg_add = models.CharField("телеграм адрес", max_length=56, default="empty")
    name = models.CharField("имя", max_length=56, default="empty")
    second_name = models.CharField("фамилия", max_length=56, default="empty")
    third_name =models.CharField("отчество", max_length=56, default="empty")
    shop = models.ForeignKey(Shop, on_delete=models.SET_DEFAULT, default=1)
    position = models.ForeignKey(Position, on_delete=models.SET_DEFAULT, default=1)
    created = models.DateTimeField("дата регистрации", auto_now_add=True)
    valid = models.BooleanField("валидация", default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "карточка сотрудника"
        verbose_name_plural = "карточки сотрудников"
        ordering = ['-created']


    