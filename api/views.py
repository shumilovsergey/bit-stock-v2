from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import TelegramUsers
from .models import UserCard
from .models import Shop

from server.const import BOT_NAME
from server.const import HOST_DNS

class Main(View):
    def get(self, request):
        bot_name = BOT_NAME
        session_id = request.session["session_id"]
        auth = request.session["auth"]
        return render(request, 'main.html', {"bot_name":bot_name, "session_id":session_id, "auth":auth, "dns":HOST_DNS})
    
class Login(View):
    def get(self, request):
        session_id = request.session["session_id"]
        telegram_login_url = f"https://t.me/{BOT_NAME}?start={session_id}"
        return redirect(telegram_login_url)

class AuthCheck(View):
    def get(self, request):
        session_id = request.GET.get('session_id')
        if TelegramUsers.objects.filter(session_id=session_id).exists():
            return JsonResponse({'result': True})
        else:
            return JsonResponse({'result': False})

class Logout(View):
    def get(self, request):
        session_id = request.session["session_id"]
        if TelegramUsers.objects.filter(session_id=session_id).exists():
            user = TelegramUsers.objects.get(session_id=session_id)
            user.session_id = "None"
            user.save()

        request.session["session_id"]=None
        request.session["auth"]=None
        request.session["name"]=None
        request.session["org_select"]=None
        return redirect("/")
    
# UserCard
class Card(View):
    def get(self, request):
        session_id = request.session["session_id"]

        if not TelegramUsers.objects.filter(session_id=session_id).exists():
            info = "вы не авторизовались"
            return render(request, 'info.html', {"info":info})
        
        user = TelegramUsers.objects.get(session_id=session_id)    

        if not UserCard.objects.filter(tg_id=user.tg_id).exists():
            user_card = UserCard.objects.create(tg_id=user.tg_id)
            user_card.save()

        user_card = UserCard.objects.get(tg_id=user.tg_id)
        return render(request, 'user_card/card.html', {"user_card":user_card})

    def post(self, request):

        session_id = request.session["session_id"]        
        user = TelegramUsers.objects.get(session_id=session_id)
        user_card = UserCard.objects.get(tg_id=user.tg_id)
        user_card.name = request.POST["name"]
        user_card.second_name = request.POST["second_name"]
        user_card.third_name = request.POST["third_name"]
        user_card.tg_add =request.POST["tg_add"].replace("@", "")
        user_card.save()

        return redirect("/user_card/")
        
# add_book
class AddBook(View):
    def get(self, request):
        add_book = []
        shops = Shop.objects.all()
        for shop in shops:
            user_cards = shop.usercard_set.all()
            for user_card in user_cards:
                add_book.append(user_card)

        return render(request, 'user_card/add_book.html', {'add_book':add_book})

