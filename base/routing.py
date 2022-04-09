from django.urls import re_path

from base import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<roomId>\w+)/$', consumers.ChatConsumer.as_asgi()),
]