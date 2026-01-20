from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Like, Follow, UserProfile
from .forms import PostCreateForm, CommentCreateForm, UserProfileForm


def home(request):
    """ホームタイムライン"""
    if request.user.is_authenticated:
        # フォローしているユーザーの投稿を取得
        following_users = Follow.objects.filter(follower=request.user).values_list(
            "following", flat=True
        )
        posts = (
            Post.objects.filter(Q(author__in=following_users) | Q(author=request.user))
            .select_related("author")
            .prefetch_related("likes", "comments")
        )
    else:
        # 未ログインユーザーには全ての投稿を表示
        posts = (
            Post.objects.all()
            .select_related("author")
            .prefetch_related("likes", "comments")
        )

    # ページネーション
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    # 各投稿にいいね状態を追加
    if request.user.is_authenticated:
        for post in posts:
            post.user_has_liked = post.is_liked_by(request.user)

    # 投稿フォーム
    form = PostCreateForm() if request.user.is_authenticated else None

    context = {
        "posts": posts,
        "form": form,
    }
    return render(request, "work13/home.html", context)


@login_required
def create_post(request):
    """投稿作成"""
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "投稿が作成されました！")
            return redirect("work13:home")
    else:
        form = PostCreateForm()

    context = {
        "form": form,
    }
    return render(request, "work13/create_post.html", context)


def post_detail(request, post_id):
    """投稿詳細表示"""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().select_related("user")

    # コメントフォーム
    comment_form = CommentCreateForm() if request.user.is_authenticated else None

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "work13/post_detail.html", context)


@login_required
@require_POST
def toggle_like(request, post_id):
    """いいねの切り替え（Ajax対応）"""
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        # 既にいいねしている場合は削除
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse(
        {
            "liked": liked,
            "like_count": post.like_count(),
        }
    )


@login_required
@require_POST
def add_comment(request, post_id):
    """コメント追加"""
    post = get_object_or_404(Post, id=post_id)
    form = CommentCreateForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            # Ajax リクエストの場合
            return JsonResponse(
                {
                    "success": True,
                    "comment": {
                        "id": comment.id,
                        "content": comment.content,
                        "user": comment.user.username,
                        "created_at": comment.created_at.strftime("%Y/%m/%d %H:%M"),
                    },
                }
            )
        else:
            messages.success(request, "コメントを追加しました！")
    else:
        messages.error(request, "コメントの追加に失敗しました。")

    return redirect("work13:post_detail", post_id=post_id)


def user_profile(request, username):
    """ユーザープロフィール表示"""
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by("-created_at")

    # フォロー状態をチェック
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()

    # 統計情報
    post_count = posts.count()
    follower_count = user.followers.count()
    following_count = user.following.count()

    context = {
        "profile_user": user,
        "posts": posts,
        "is_following": is_following,
        "post_count": post_count,
        "follower_count": follower_count,
        "following_count": following_count,
    }
    return render(request, "work13/user_profile.html", context)


@login_required
def edit_profile(request):
    """プロフィール編集"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "プロフィールを更新しました！")
            return redirect("work13:user_profile", username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)

    context = {
        "form": form,
    }
    return render(request, "work13/edit_profile.html", context)


@login_required
@require_POST
def toggle_follow(request, username):
    """フォロー・アンフォローの切り替え"""
    user_to_follow = get_object_or_404(User, username=username)

    if user_to_follow == request.user:
        messages.error(request, "自分をフォローすることはできません。")
        return redirect("work13:user_profile", username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user, following=user_to_follow
    )

    if not created:
        # 既にフォローしている場合は削除
        follow.delete()
        messages.success(
            request, f"{user_to_follow.username}のフォローを解除しました。"
        )
    else:
        messages.success(request, f"{user_to_follow.username}をフォローしました！")

    return redirect("work13:user_profile", username=username)


@login_required
@require_POST
def delete_post(request, post_id):
    """投稿削除"""
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, "この投稿を削除する権限がありません。")
        return redirect("work13:post_detail", post_id=post_id)

    post.delete()
    messages.success(request, "投稿を削除しました。")
    return redirect("work13:home")


def explore(request):
    """投稿を探索"""
    posts = (
        Post.objects.all()
        .select_related("author")
        .prefetch_related("likes", "comments")
    )

    # 検索機能
    search_query = request.GET.get("search")
    if search_query:
        posts = posts.filter(
            Q(caption__icontains=search_query)
            | Q(author__username__icontains=search_query)
        )

    # ページネーション
    paginator = Paginator(posts, 12)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    context = {
        "posts": posts,
        "search_query": search_query,
    }
    return render(request, "work13/explore.html", context)


@login_required
def following_list(request, username):
    """フォローリスト"""
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user).select_related("following")

    context = {
        "profile_user": user,
        "following": following,
    }
    return render(request, "work13/following_list.html", context)


@login_required
def followers_list(request, username):
    """フォロワーリスト"""
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user).select_related("follower")

    context = {
        "profile_user": user,
        "followers": followers,
    }
    return render(request, "work13/followers_list.html", context)
