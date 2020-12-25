from django.urls import path
from .views import *

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]

urlpatterns = [
    path('getTickData/', get_tick_data),
    path('getImg/', get_pixels),
    path('getImgByDate/', get_pixels_by_date),
    path('img/'),
]