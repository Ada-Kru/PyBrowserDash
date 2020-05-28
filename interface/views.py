from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads, dumps, JSONDecodeError
from .validation import new_msg_validator, seen_messages_validator
from validx import exc
from datetime import datetime, timezone
from subprocess import call as sp_call
from .clean_message import clean_message
from .models import Message
from .funcs import make_unused_id

try:
    from PyBrowserDash.local_config import WOL_COMMAND
except ImportError:
    from PyBrowserDash.config import WOL_COMMAND


unseen = {}


def index(request):
    for connection in request.scope["ws_connections"]:
        connection.send_msg("testin")
    return HttpResponse("...")


@csrf_exempt
def messages_new(request):
    if request.method != "POST":
        raise Http404("Not Found")

    try:
        msg = loads(request.body)
        new_msg_validator(msg)
        clean_message(msg)
        if msg["type"] == "log":
            msg["seen"] = True
        # print(msg)

        Message(
            sender=msg["sender"],
            text=msg["text"],
            type=msg["type"],
            time=msg["time"],
            data=msg["data"],
        ).save()
        if not msg["seen"]:
            msg_id = make_unused_id(unseen)
            unseen[msg_id] = msg
            for connection in request.scope["ws_connections"]:
                connection.send_msg(dumps({"new_messages": {msg_id: msg}}))

    except (exc.ValidationError, JSONDecodeError) as err:
        return JsonResponse({"error": str(err)})

    return JsonResponse({"error": None}, status=201)


@csrf_exempt
def messages_unseen(request):
    if request.method == "POST":
        try:
            seen_ids = loads(request.body)
            seen_messages_validator(seen_ids)
            for seen_id in seen_ids:
                unseen.pop(seen_id, None)

        except (exc.ValidationError, JSONDecodeError) as err:
            return JsonResponse({"error": str(err)})

    return JsonResponse({"error": None, "messages": unseen})


@csrf_exempt
def messages_clear_unseen(request):
    if request.method == "POST":
        unseen.clear()
        return JsonResponse({"error": None})


def messages_history(request, limit):
    db_messages = Message.objects.order_by("time")[:limit]
    messages = []
    for db_msg in db_messages:
        messages.append(
            {
                "sender": db_msg.sender,
                "text": db_msg.text,
                "type": db_msg.type,
                "time": db_msg.time,
                "data": db_msg.data,
            }
        )
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
