from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="top"),
    path("index/", views.index, name="index"),
    path("list/", views.list, name="list"),
]
