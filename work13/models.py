from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os


class UserProfile(models.Model):
    """ユーザープロフィール拡張モデル"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    bio = models.TextField(max_length=500, blank=True, verbose_name="自己紹介")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="プロフィール画像")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日")
    
    def __str__(self):
        return f"{self.user.username}のプロフィール"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            # プロフィール画像をリサイズ
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
    
    class Meta:
        verbose_name = "ユーザープロフィール"
        verbose_name_plural = "ユーザープロフィール"


class Post(models.Model):
    """投稿モデル"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="投稿者")
    image = models.ImageField(upload_to='posts/', verbose_name="画像")
    caption = models.TextField(max_length=2000, blank=True, verbose_name="キャプション")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="投稿日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    def __str__(self):
        return f"{self.author.username}の投稿 - {self.created_at.strftime('%Y/%m/%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            # 投稿画像をリサイズ
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    def like_count(self):
        """いいね数を取得"""
        return self.likes.count()
    
    def comment_count(self):
        """コメント数を取得"""
        return self.comments.count()
    
    def is_liked_by(self, user):
        """特定のユーザーがいいねしているかチェック"""
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False
    
    class Meta:
        verbose_name = "投稿"
        verbose_name_plural = "投稿"
        ordering = ['-created_at']


class Like(models.Model):
    """いいねモデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name="投稿")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="いいね日時")
    
    def __str__(self):
        return f"{self.user.username} → {self.post.author.username}の投稿"
    
    class Meta:
        verbose_name = "いいね"
        verbose_name_plural = "いいね"
        unique_together = ('user', 'post')  # 同じユーザーが同じ投稿に複数いいねできないように
        ordering = ['-created_at']


class Comment(models.Model):
    """コメントモデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="投稿")
    content = models.TextField(max_length=1000, verbose_name="コメント内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="コメント日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}..."
    
    class Meta:
        verbose_name = "コメント"
        verbose_name_plural = "コメント"
        ordering = ['created_at']


class Follow(models.Model):
    """フォローモデル"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name="フォローする人")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name="フォローされる人")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="フォロー日時")
    
    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"
    
    class Meta:
        verbose_name = "フォロー"
        verbose_name_plural = "フォロー"
        unique_together = ('follower', 'following')  # 同じユーザーを複数回フォローできないように
        ordering = ['-created_at']


# シグナルを使ってUserが作成されたときに自動的にUserProfileを作成
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
