from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="top"),
    path("index/", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("edit/<int:id>/", views.edit, name="edit"),
]
