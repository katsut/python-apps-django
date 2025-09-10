from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "work05/index.html")


def list(request):

    total = 1111
    return HttpResponse("Hello, world. You're at the work05 list." + str(total))
