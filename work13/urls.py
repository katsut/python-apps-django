from django.urls import path
from . import views

app_name = 'work13'

urlpatterns = [
    # ホーム・基本機能
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    
    # 投稿関連
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    
    # ユーザー関連
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('user/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('user/<str:username>/following/', views.following_list, name='following_list'),
    path('user/<str:username>/followers/', views.followers_list, name='followers_list'),
    
    # プロフィール編集
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
