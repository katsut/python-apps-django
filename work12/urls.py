from django.urls import path
from . import views

app_name = 'work12'

urlpatterns = [
    path('', views.chat_room, name='chat_room'),
]
