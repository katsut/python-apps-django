from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message


@login_required
def chat_room(request):
    messages = Message.objects.all()[:50]  # 最新50件のメッセージを取得
    return render(request, 'work12/chat.html', {'messages': messages})
