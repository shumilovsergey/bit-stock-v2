from django.contrib import admin
from .models import TelegramUsers
from .models import UserCard
from .models import Shop
from .models import TelegramUsers
from .models import Categories
from .models import Brands
from .models import Products


admin.site.register(TelegramUsers)
admin.site.register(UserCard)
admin.site.register(Shop)
admin.site.register(Categories)
admin.site.register(Brands)
admin.site.register(Products)


