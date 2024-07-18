from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import TelegramUsers
from .models import UserCard
from .models import Shop
from .models import Categories

from server.const import BOT_NAME
from server.const import HOST_DNS

class TestView(View):
    def get(self, request):
        result = []
        return render(request, 'test.html')
    



    