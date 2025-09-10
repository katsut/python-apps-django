from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="top"),
    path("index/", views.index, name="index"),
    path("reiwa/", views.reiwa, name="reiwa"),
    # path("calculator/", views.calculator, name="calculator"),
    # path("bmi/", views.bmi, name="bmi"),
    # path("warikan/", views.warikan, name="warikan"),
    # path("tani/", views.tani, name="tani"),
    # path("chokin/", views.chokin, name="chokin"),
    # path("omikuji/", views.omikuji, name="omikuji"),
]
