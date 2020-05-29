"""
ASGI config for PyBrowserDash project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from PyBrowserDash.websocket import websocket_app
from asyncio import create_task
from .background_tasks import BackgroundTasks

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyBrowserDash.settings")

django_app = get_asgi_application()
bg_tasks = BackgroundTasks()


async def application(scope, receive, send):
    if not bg_tasks.tasks_started():
        create_task(bg_tasks.start_tasks())
    scope["background_tasks"] = bg_tasks
    scope_type = scope["type"]

    if scope_type == "http":
        await django_app(scope, receive, send)
    elif scope_type == "websocket":
        await websocket_app(scope, receive, send)
    elif scope_type == "lifespan":
        while True:
            message = await receive()
            msg_type = message["type"]
            if msg_type == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif msg_type == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})

    else:
        raise NotImplementedError(f"Unknown scope: {scope_type}")
