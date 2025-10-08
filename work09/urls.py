from django.urls import path
from . import views

app_name = 'work09'

urlpatterns = [
    path("", views.index, name="top"),
    path("edit/<int:todo_id>/", views.edit, name="edit"),
    path("update/<int:todo_id>/", views.update, name="update"),
    path("delete/<int:todo_id>/", views.delete, name="delete"),
    path("toggle/<int:todo_id>/", views.toggle_complete, name="toggle_complete"),
]
