from django.db import models
from django.utils import timezone

class TelegramUsers(models.Model):
    session_id = models.CharField(max_length=56, unique=True)
    tg_id = models.CharField(max_length=56, default="no-auth")
    name = models.CharField(max_length=56, default="no-auth")
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.tg_id
    class Meta:
        ordering = ['-created']

class UserCard(models.Model):
    tg_id = models.CharField("телеграм id", max_length=56)
    tg_add = models.CharField("телеграм адрес", max_length=56, default="empty")
    name = models.CharField("имя", max_length=56, default="empty")
    second_name = models.CharField("фамилия", max_length=56, default="empty")
    third_name =models.CharField("отчество", max_length=56, default="empty")
    shop = models.CharField("адрес магазина", max_length=56, default="empty")
    position = models.CharField("должность", max_length=56, default="empty")
    valid = models.BooleanField("валидация", default=False)
    created = models.DateTimeField("дата регистрации", auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']

    