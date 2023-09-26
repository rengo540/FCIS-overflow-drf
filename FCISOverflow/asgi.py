"""
ASGI config for FCISOverflow project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from group_chat.middlewares import JwtOrSessionAuthMiddlewareStack
from group_chat.routing import websocker_urlpatterns
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FCISOverflow.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            JwtOrSessionAuthMiddlewareStack(URLRouter(websocker_urlpatterns))
        ),
    }
)