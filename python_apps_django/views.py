from django.shortcuts import render


def index(request):
    """プロジェクトのトップページ"""
    return render(request, "index.html")
