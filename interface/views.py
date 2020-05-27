from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from json import loads, dumps, JSONDecodeError
from .validation import new_msg_validator
from validx import exc
from .clean_message import clean_message
from .models import Message


def index(request):
    # print(request.scope)
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
        print(msg)

    except (exc.ValidationError, JSONDecodeError) as err:
        return HttpResponse(dumps({"error": str(err)}))

    return HttpResponse(dumps({"error": None}), status=201)


def messages_get(request, limit):
    messages = Message.objects.order_by("msg_time")[:limit]
    for msg in messages:
        print(msg.msg_sender, msg.msg_text)
    return HttpResponse(f"Got {len(messages)} messages.")
