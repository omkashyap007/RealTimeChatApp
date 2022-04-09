import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter , URLRouter 
from base import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chatapp.settings')

application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application() ,
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns 
            )
        )
    }
)
