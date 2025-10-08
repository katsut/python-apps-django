from django.shortcuts import render
import random

# Create your views here.


def index(request):

    return render(request, "work07/index.html")


def omikuji(request):
    # 初回開いたときはresultはNone
    result = None
    if request.method == "POST":
        result = random.choice(["大吉", "中吉", "小吉", "吉", "末吉", "凶"])
        print(result)
    return render(request, "work07/omikuji.html", {"result": result})
