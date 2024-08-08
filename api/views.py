from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

from .models import TelegramUsers
from .models import UserCard
from .models import Shop
from .models import Categories
from .models import Brands
from .models import Products
from .models import Deals

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
        return redirect("/")
    
# UserCard
class Card(View):
    def get(self, request):
        session_id = request.session["session_id"]

        if not TelegramUsers.objects.filter(session_id=session_id).exists():
            info = "вы не авторизовались"
            return render(request, 'info.html', {"info":info})
        
        user = TelegramUsers.objects.get(session_id=session_id)

        if not Shop.objects.exists():
            shop = Shop.objects.create(name="unsort")
            shop.save()

        if not UserCard.objects.filter(tg_id=user.tg_id).exists():
            user_card = UserCard.objects.create(tg_id=user.tg_id)
            user_card.save()

        user_card = UserCard.objects.get(tg_id=user.tg_id)

        return render(request, 'user_card/card.html', {"user_card":user_card, "tg_id":user.tg_id})

    def post(self, request):

        session_id = request.session["session_id"]        
        user = TelegramUsers.objects.get(session_id=session_id)
        user_card = UserCard.objects.get(tg_id=user.tg_id)
        user_card.name = request.POST["name"]
        user_card.second_name = request.POST["second_name"]
        user_card.third_name = request.POST["third_name"]
        user_card.tg_add =request.POST["tg_add"].replace("@", "")
        user_card.save()

        return redirect("/")
        
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

# products
class ProductList(View):
    def get(self, request):
        product_list = []
        exist_lis = []
        unexist_list = []

        categories = Categories.objects.all()
        for category in categories:
            brands = category.brands_set.all()
            for brand in brands:
                products = brand.products_set.all()
                for product in products:
                    if product.amount > 0:
                        exist_lis.append(product)
                    else:
                        unexist_list.append(product)

        product_list = exist_lis + unexist_list
        return render(request, 'product/product_list.html', {'product_list':product_list})
    
    def post(self, request):
        category_input = request.POST["category"].lower()
        brand_input = request.POST["brand"].lower()
        product_input = request.POST["product"].lower()
        category, created = Categories.objects.get_or_create(name=category_input)
        brand, created = Brands.objects.get_or_create(name=brand_input, category=category)

        if Products.objects.filter(name=product_input, brand=brand.id).exists():
            info = "такая карточка товара уже существует! карточка товара должна быть уникальной - операция отменена!"
            return render(request, 'info.html', {'info':info})
        else:
            product = Products.objects.create(name=product_input, brand=brand)
            product.save()
        return redirect("/product_list/")
    
# deal

class DealCreate(View):
    def get(self, request):
        return redirect("/")
    
    def post(self, request):
        string = request.POST.get('product_ids')
        product_id_list = json.loads(string)
        if len(product_id_list) == 0:
            return redirect("/")
        
        products_choisen= []
        for product_id in product_id_list:
            if not Products.objects.filter(id=product_id).exists():
                info = "Сделка не может быть создана, одного из продуктов нет на складе"
                return render(request, 'info.html', {'info':info})
            else:
                product = Products.objects.get(id=product_id)
                products_choisen.append(product)

        return render(request, 'deal/deal_create.html', {"products_choisen":products_choisen})
    
class DealList(View):
    def get(self, request):
        deal_list = []
        session_id = request.session["session_id"]        
        user = TelegramUsers.objects.get(session_id=session_id)
        
        if not UserCard.objects.filter(tg_id=user.tg_id).exists():
            info = "нужно заполнить карточку сотрудника!"
            return render(request, 'info.html', {'info':info})

        user_card = UserCard.objects.get(tg_id=user.tg_id)
        if user.access != 3:
            shop = user_card.shop
            deal_list = Deals.objects.filter(shop=shop)
        else:
            deal_list = Deals.objects.all()

        return render(request, 'deal/deal_list.html', {'deal_list':deal_list})
    
    def post(self, request):
        # lists
        ids = request.POST.getlist('id')
        product_prices = request.POST.getlist('product_price')
        amounts = request.POST.getlist('amount')

        # single
        type = request.POST["type"]
        session_id = request.session["session_id"]        
        user = TelegramUsers.objects.get(session_id=session_id)

        if not UserCard.objects.filter(tg_id=user.tg_id).exists():
            info = "нужно заполнить карточку сотрудника!"
            return render(request, 'info.html', {'info':info})

        user_card = UserCard.objects.get(tg_id=user.tg_id)
        if user_card.tg_add == "empty":
            info = "нужно заполнить карточку сотрудника!"
            return render(request, 'info.html', {'info':info})

        tg_id = user_card.tg_id
        tg_add = user_card.tg_add
        user_name = user_card.second_name
        shop = user_card.shop.name

        # loop
        for id, product_price, amount in zip(ids, product_prices, amounts):
            product = Products.objects.get(id=id)

            if type == "-":
                product.amount = product.amount + int(amount)
            elif type == "+":
                product.amount = product.amount - int(amount)
            product.save()

            brand = product.brand.name
            category = product.brand.category.name
            total_price = int(amount) * int(product_price)

            deal = Deals.objects.create(
                tg_id = tg_id,
                tg_add = tg_add,
                user_name = user_name,
                shop = shop,
                category = category,
                brand = brand,
                product = product.name,
                amount = int(amount),
                product_price = int(product_price),
                tota_price = int(total_price),
                type = type,
            )
            deal.save()
        return redirect("/deal_list/")
    
