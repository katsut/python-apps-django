import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Post, Like, Comment


class LiveFeedConsumer(AsyncWebsocketConsumer):
    """リアルタイムフィード用のWebSocketコンシューマー"""
    
    async def connect(self):
        self.room_name = 'live_feed'
        self.room_group_name = f'feed_{self.room_name}'

        # グループに参加
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # グループから離脱
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'new_post':
            # 新しい投稿があったことをブロードキャスト
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'new_post_notification',
                    'post_id': text_data_json.get('post_id'),
                    'author': text_data_json.get('author'),
                    'message': '新しい投稿があります！'
                }
            )

    async def new_post_notification(self, event):
        # フロントエンドに新しい投稿の通知を送信
        await self.send(text_data=json.dumps({
            'type': 'new_post',
            'post_id': event['post_id'],
            'author': event['author'],
            'message': event['message']
        }))


class PostConsumer(AsyncWebsocketConsumer):
    """個別投稿のリアルタイム更新用WebSocketコンシューマー"""
    
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'post_{self.post_id}'

        # グループに参加
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # グループから離脱
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'like_update':
            # いいね数の更新をブロードキャスト
            post_id = text_data_json.get('post_id')
            user_id = text_data_json.get('user_id')
            
            # データベースから最新のいいね数を取得
            like_count = await self.get_like_count(post_id)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'like_count_update',
                    'post_id': post_id,
                    'like_count': like_count,
                    'user_id': user_id
                }
            )

        elif message_type == 'new_comment':
            # 新しいコメントをブロードキャスト
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'comment_notification',
                    'post_id': text_data_json.get('post_id'),
                    'comment_id': text_data_json.get('comment_id'),
                    'author': text_data_json.get('author'),
                    'content': text_data_json.get('content'),
                    'created_at': text_data_json.get('created_at')
                }
            )

    async def like_count_update(self, event):
        # いいね数の更新をフロントエンドに送信
        await self.send(text_data=json.dumps({
            'type': 'like_update',
            'post_id': event['post_id'],
            'like_count': event['like_count'],
            'user_id': event['user_id']
        }))

    async def comment_notification(self, event):
        # 新しいコメントをフロントエンドに送信
        await self.send(text_data=json.dumps({
            'type': 'new_comment',
            'post_id': event['post_id'],
            'comment_id': event['comment_id'],
            'author': event['author'],
            'content': event['content'],
            'created_at': event['created_at']
        }))

    @database_sync_to_async
    def get_like_count(self, post_id):
        """投稿のいいね数を取得"""
        try:
            post = Post.objects.get(id=post_id)
            return post.like_count()
        except Post.DoesNotExist:
            return 0

    @database_sync_to_async
    def get_comment_count(self, post_id):
        """投稿のコメント数を取得"""
        try:
            post = Post.objects.get(id=post_id)
            return post.comment_count()
        except Post.DoesNotExist:
            return 0


class NotificationConsumer(AsyncWebsocketConsumer):
    """ユーザー通知用WebSocketコンシューマー"""
    
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
        else:
            self.room_group_name = f'user_{self.user.id}_notifications'

            # グループに参加
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            # グループから離脱
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # 通知の既読処理など
        pass

    async def notification_message(self, event):
        # 通知をフロントエンドに送信
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification_type': event['notification_type'],
            'message': event['message'],
            'from_user': event.get('from_user'),
            'post_id': event.get('post_id')
        }))
