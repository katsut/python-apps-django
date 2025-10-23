import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 認証確認
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_name = "chat"
        self.room_group_name = f"chat_{self.room_name}"

        # チャットグループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # チャットグループから離脱
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # 認証されたユーザーの名前を使用
        user = self.scope["user"]
        username = user.username if user.is_authenticated else "匿名"

        # メッセージをデータベースに保存
        await self.save_message(user, username, message)

        # グループの全員にメッセージを送信
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # WebSocketにメッセージを送信
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, user, username, message):
        Message.objects.create(
            user=user if user.is_authenticated else None,
            username=username,
            content=message,
        )
