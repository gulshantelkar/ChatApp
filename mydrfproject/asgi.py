# mydrfproject/asgi.py

import os
from sys import path
path.append(os.getcwd()+'/mydrfproject')
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydrfproject.settings')
import django
django.setup()
from chatapp.routing import websocket_urlpatterns  
from .middleware import TokenAuthMiddleware



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),  
})
