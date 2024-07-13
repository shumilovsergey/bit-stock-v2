from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import connection, transaction
from .models import Shop
from .models import Position

@receiver(post_delete, sender=Shop)
def reset_shop_sequence(sender, **kwargs):
    if not Shop.objects.exists():
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='api_shop'")

@receiver(post_delete, sender=Position)
def reset_shop_sequence(sender, **kwargs):
    if not Position.objects.exists():
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='api_position'")