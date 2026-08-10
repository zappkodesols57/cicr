from .views import reverse_geocode
from django.urls import path
from .views import *

urlpatterns = [
    path('chatbot/chat/', chat_page, name='chat_page'),
    path('chatbot/response/', chatbot_response, name='chatbot_response'),
    path('chatbot/webhook/', webhook, name='webhook'),
    path('chatbot/reverse-geocode/', reverse_geocode, name='reverse_geocode'),
    path('chatbot/set-location/', set_location, name='set_location'),
    path("chatbot/weather/", live_weather),
]
