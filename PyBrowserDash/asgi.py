"""
ASGI config for PyBrowserDash project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from PyBrowserDash.websocket import websocket_app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyBrowserDash.settings")

django_app = get_asgi_application()


async def application(scope, receive, send):
    scope_type = scope["type"]
    if scope_type == "http":
        await django_app(scope, receive, send)
    elif scope_type == "websocket":
        await websocket_app(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope: {scope_type}")
