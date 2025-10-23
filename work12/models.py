from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100, default='匿名')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        
    def __str__(self):
        return f'{self.username}: {self.content[:50]}'
