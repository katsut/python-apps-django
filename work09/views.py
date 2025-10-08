from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Todo
from .forms import TodoCreateForm, TodoUpdateForm

# Create your views here.


def index(request):
    """TODO一覧画面（Read）と新規作成（Create）"""
    # ソートパラメータを取得
    sort_by = request.GET.get("sort", "created_at")  # デフォルトは登録日
    order = request.GET.get("order", "desc")  # デフォルトは降順
    
    # フィルタパラメータを取得
    filter_by = request.GET.get("filter", "all")  # デフォルトは全て表示

    # ソートフィールドの検証
    valid_sort_fields = ["created_at", "due_date", "title"]
    if sort_by not in valid_sort_fields:
        sort_by = "created_at"

    # 順序の検証
    if order not in ["asc", "desc"]:
        order = "desc"
        
    # フィルタの検証
    valid_filters = ["all", "incomplete", "complete"]
    if filter_by not in valid_filters:
        filter_by = "all"

    # フィルタ適用
    if filter_by == "incomplete":
        todos = Todo.objects.filter(is_completed=False)
    elif filter_by == "complete":
        todos = Todo.objects.filter(is_completed=True)
    else:
        todos = Todo.objects.all()

    # ソート用のフィールド名を構築
    order_by = f"{'-' if order == 'desc' else ''}{sort_by}"

    # due_dateでソートする場合、NULLを最後に配置
    if sort_by == "due_date":
        if order == "asc":
            todos = todos.order_by("due_date", "created_at")
        else:
            todos = todos.order_by("-due_date", "-created_at")
    else:
        todos = todos.order_by(order_by)

    today = timezone.now().date()

    if request.method == "POST":
        form = TodoCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "タスクが作成されました。")
            return redirect("work09:top")
    else:
        form = TodoCreateForm()

    # ソート情報を日本語に変換
    sort_labels = {"created_at": "登録日", "due_date": "期限日", "title": "タスク名"}
    order_labels = {"asc": "昇順", "desc": "降順"}
    filter_labels = {"all": "全て", "incomplete": "未完了のみ", "complete": "完了済みのみ"}

    context = {
        "todos": todos,
        "form": form,
        "today": today,
        "current_sort": sort_by,
        "current_order": order,
        "current_filter": filter_by,
        "sort_label": sort_labels.get(sort_by, "登録日"),
        "order_label": order_labels.get(order, "降順"),
        "filter_label": filter_labels.get(filter_by, "全て"),
    }
    return render(request, "work09/index.html", context)


def edit(request, todo_id):
    """タスクの修正画面（Update form display）"""
    todo = get_object_or_404(Todo, id=todo_id)
    form = TodoUpdateForm(instance=todo)

    context = {
        "todo": todo,
        "form": form,
    }
    return render(request, "work09/edit.html", context)


def update(request, todo_id):
    """タスクの修正処理（Update processing）"""
    todo = get_object_or_404(Todo, id=todo_id)

    if request.method == "POST":
        form = TodoUpdateForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "タスクが更新されました。")
            return redirect("work09:top")

    return redirect("work09:edit", todo_id=todo_id)


def delete(request, todo_id):
    """タスクの削除（Delete）"""
    todo = get_object_or_404(Todo, id=todo_id)

    if request.method == "POST":
        todo.delete()
        messages.success(request, "タスクが削除されました。")

    return redirect("work09:top")


def toggle_complete(request, todo_id):
    """タスクの完了状態を切り替え"""
    todo = get_object_or_404(Todo, id=todo_id)

    if request.method == "POST":
        todo.is_completed = not todo.is_completed
        todo.save()

        if todo.is_completed:
            messages.success(request, f"「{todo.title}」を完了にしました。")
        else:
            messages.success(request, f"「{todo.title}」を未完了にしました。")

    return redirect("work09:top")
