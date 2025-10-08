from django.shortcuts import redirect, render

from work08 import models
from work08.forms import MemoForm

# Create your views here.


# memo app views
def index(request):
    memos = models.Memo.objects.all().order_by("-created_at")
    return render(request, "work08/index.html", {"memos": memos})


def create(request):
    # 空のデータを登録
    memo = models.Memo.objects.create()
    return redirect("edit", id=memo.id)


def edit(request, id: int):
    memo = models.Memo.objects.get(id=id)

    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            memo.title = form.cleaned_data.get("title")
            memo.content = form.cleaned_data.get("content")
            memo.save()
            return redirect("index")

    form = MemoForm(initial={"title": memo.title, "content": memo.content})
    return render(request, "work08/edit.html", {"form": form, "memo_id": memo.id})
