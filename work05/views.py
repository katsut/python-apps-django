from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    name = "Django"
    age = 7
    return render(request, "work05/index.html", {"name": name, "age": age})


def list(request):

    total = 1111
    return HttpResponse("Hello, world. You're at the work05 list." + str(total))
