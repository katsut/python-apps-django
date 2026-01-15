from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, UserProfile


class PostCreateForm(forms.ModelForm):
    """投稿作成フォーム"""
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'キャプションを入力してください...',
                'rows': 3
            }),
        }
        labels = {
            'image': '画像',
            'caption': 'キャプション',
        }


class CommentCreateForm(forms.ModelForm):
    """コメント作成フォーム"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'コメントを入力...',
            }),
        }
        labels = {
            'content': '',
        }


class UserProfileForm(forms.ModelForm):
    """ユーザープロフィール編集フォーム"""
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '自己紹介を入力してください...',
                'rows': 4
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'bio': '自己紹介',
            'avatar': 'プロフィール画像',
        }


class CustomUserCreationForm(UserCreationForm):
    """カスタムユーザー作成フォーム"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # プレースホルダーを設定
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['first_name'].widget.attrs['placeholder'] = '名前'
        self.fields['last_name'].widget.attrs['placeholder'] = '苗字'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
