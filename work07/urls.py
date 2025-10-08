from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="top"),
    path("index/", views.index, name="index"),
    path("omikuji/", views.omikuji, name="omikuji"),
]
