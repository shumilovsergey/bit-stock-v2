from django.urls import path
from .views import Main
from .views import Login
from .views import Logout
from .views import AuthCheck
from .views import Card
from .views import AddBook


app_name = 'api'
urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('auth_check/', AuthCheck.as_view(), name='auth_check'),
    # user_card
    path('user_card/', Card.as_view(), name='user_card'),
    # add_book
    path('add_book/', AddBook.as_view(), name='add_book'),
]