
from django.urls import path
from . import views
from .consumers import ChatConsumer

from .views import register_user, user_login, user_logout, get_online_users,start_chat  

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('online-users/', get_online_users, name='get_online_users'),
    path('chat/start/', start_chat, name='start_chat'),
]
