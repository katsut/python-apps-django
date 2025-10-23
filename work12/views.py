from django.shortcuts import render
from .models import Message


def chat_room(request):
    messages = Message.objects.all()[:50]  # 最新50件のメッセージを取得
    return render(request, 'work12/chat.html', {'messages': messages})
