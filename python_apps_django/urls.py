"""
URL configuration for python_apps_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import urls

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("work05/", include("work05.urls")),
    path("work06/", include("work06.urls")),
    path("work07/", include("work07.urls")),
    path("work08/", include("work08.urls")),
    path("work09/", include("work09.urls")),
    path("work10/", include("work10.urls")),
    path("work11/", include("work11.urls")),
    # 認証関連（プロジェクト全体）
    path(
        "login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/login/"), name="logout"),
    path(
        "signup/",
        CreateView.as_view(
            form_class=UserCreationForm,
            template_name="registration/signup.html",
            success_url=reverse_lazy("login"),
        ),
        name="signup",
    ),
]
