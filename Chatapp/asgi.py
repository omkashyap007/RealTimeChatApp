from django.core.asgi import get_asgi_application
django_asgi_application = get_asgi_application()
import os
from channels.routing import ProtocolTypeRouter , URLRouter 
from channels.auth import AuthMiddlewareStack
from base import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chatapp.settings')

application = ProtocolTypeRouter(
    {
        "http" : django_asgi_application,
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns 
            )
        )
    }
)
