"""
ASGI config for python_apps_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_apps_django.settings")

# Django ASGIアプリケーションを先に初期化
django_asgi_app = get_asgi_application()

# Djangoが完全に初期化された後にwork12.routingをインポート
import work12.routing  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # 認証を必須にする場合はAuthMiddlewareStackを使用
        "websocket": AuthMiddlewareStack(
            URLRouter(work12.routing.websocket_urlpatterns)
        ),
    }
)
