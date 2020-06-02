from django.http import (
    HttpResponse,
    Http404,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from json import loads, JSONDecodeError
from .validation import new_msg_validator, seen_messages_validator
from validx import exc
from datetime import datetime, timezone
from time import time
from subprocess import call as sp_call
from ipaddress import ip_address
from .clean_message import clean_message
from .message_types import DELAYED_REPEAT_MESSAGE
from .all_message_types import ALL_MSG_TYPES
from .models import Message
from .funcs import make_unused_id, get_client_ip

try:
    from PyBrowserDash.local_config import WOL_COMMAND, USE_CUSTOM_STYLES
except ImportError:
    from PyBrowserDash.config import WOL_COMMAND, USE_CUSTOM_STYLES


MAX_REPEAT_DELAY = 300


def index(request):
    if ip_address(get_client_ip(request)).is_global:
        return HttpResponseBadRequest("")

    template = loader.get_template("interface/index.html")
    context = {"use_custom_styles": USE_CUSTOM_STYLES}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def messages_new(request):
    if request.method != "POST":
        raise HttpResponseBadRequest("GET not allowed.")

    try:
        bg = request.scope["background_tasks"]
        msg = loads(request.body)
        new_msg_validator(msg)
        clean_message(msg)

        Message(
            sender=msg["sender"],
            text=msg["text"],
            type=msg["type"],
            time=msg["time"],
            data=msg["data"],
        ).save()
        if not msg["seen"]:
            msg_id = make_unused_id(bg.unseen)
            bg.unseen[msg_id] = msg
            bg.send_all_websockets({"new_msg": {msg_id: msg}})

        speak_msg(msg, bg)

    except (exc.ValidationError, JSONDecodeError) as err:
        return JsonResponse({"error": str(err)})

    return JsonResponse({"error": None}, status=201)


def speak_msg(msg, bg_tasks):
    bg = bg_tasks
    do_speak = True
    if msg["alert_type"] == DELAYED_REPEAT_MESSAGE:
        now, key = time(), msg["sender"]
        if key in bg.no_repeat and now - bg.no_repeat[key] <= MAX_REPEAT_DELAY:
            do_speak = False
        else:
            bg.no_repeat[key] = now

    if do_speak and not bg.is_muted():
        override = msg["speech_override"] is not None
        bg.speak(msg["text"] if not override else msg["speech_override"])

    if len(bg.no_repeat) >= 10:
        keys, now = list(bg.no_repeat.keys), time()
        for key in keys:
            if now - bg.no_repeat[key] >= MAX_REPEAT_DELAY:
                bg.no_repeat.pop(key)


@csrf_exempt
def messages_unseen(request):
    bg = request.scope["background_tasks"]
    if request.method == "POST":
        try:
            seen_ids = loads(request.body)
            seen_messages_validator(seen_ids)
            for seen_id in seen_ids:
                bg.unseen.pop(seen_id, None)
            bg.send_all_websockets({"seen": seen_ids})

        except (exc.ValidationError, JSONDecodeError) as err:
            return JsonResponse({"error": str(err)})

    return JsonResponse({"error": None, "messages": bg.unseen})


@csrf_exempt
def messages_clear_unseen(request):
    bg = request.scope["background_tasks"]
    if request.method == "POST":
        bg.unseen.clear()
        bg.send_all_websockets({"unseen": {}})
        return JsonResponse({"error": None})
    else:
        return HttpResponseBadRequest(
            "Only POST requests are allowed on this endpoint."
        )


def messages_history(request, limit):
    db_messages = Message.objects.order_by("time")[:limit]
    messages, counter = {}, 0
    for db_msg in db_messages:
        msg = {
            "sender": db_msg.sender,
            "text": db_msg.text,
            "type": db_msg.type,
            "time": db_msg.time,
            "data": db_msg.data,
        }
        msg.update(ALL_MSG_TYPES[db_msg.type])
        messages[counter] = msg
        counter += 1
    return JsonResponse({"error": None, "messages": messages})


def wake_on_lan(request):
    now = (
        datetime.utcnow()
        .replace(microsecond=0, tzinfo=timezone.utc)
        .isoformat()
    )
    Message(
        sender="PyBrowserDash",
        text=f"WOL request from {request.META['REMOTE_ADDR']} at {now}",
        type="log_only",
        time=now,
        data="",
    ).save()
    sp_call(("python", WOL_COMMAND))
    return JsonResponse({"error": None})
