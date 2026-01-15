from django.contrib import admin
from .models import UserProfile, Post, Like, Comment, Follow


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'caption_preview', 'created_at', 'like_count', 'comment_count']
    list_filter = ['created_at', 'author']
    search_fields = ['author__username', 'caption']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def caption_preview(self, obj):
        """キャプションのプレビュー表示"""
        if obj.caption:
            return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
        return '(キャプションなし)'
    caption_preview.short_description = 'キャプション'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__author__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__author__username', 'content']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def content_preview(self, obj):
        """コメント内容のプレビュー表示"""
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_preview.short_description = 'コメント内容'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
