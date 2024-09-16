from django.urls import path
from config.websocket import *


from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .websocket import NotificationConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws', NotificationConsumer.as_asgi()),
]

