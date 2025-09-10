from django.shortcuts import render
from .forms import ReiwaForm

REIWA_START_YEAR = 2019  # 令和元年は2019年


def index(request):
    return render(request, "work06/index.html")


def reiwa(request):
    result = None

    if request.method == "POST":
        form = ReiwaForm(request.POST)
        if form.is_valid():
            reiwa_year = form.cleaned_data["reiwa_year"]
            seireki = REIWA_START_YEAR + reiwa_year - 1
            result = f"令和{reiwa_year}年 は 西暦 {seireki}年 です"
    else:
        form = ReiwaForm()

    return render(request, "work06/reiwa.html", {"form": form, "result": result})


def calculator(request):
    return render(request, "work06/calculator.html")


def bmi(request):
    return render(request, "work06/bmi.html")
