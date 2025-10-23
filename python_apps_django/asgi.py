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
import work12.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_apps_django.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(work12.routing.websocket_urlpatterns),
    }
)
