from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from json import loads, dumps, JSONDecodeError
from .validation import new_msg_validator
from validx import exc


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
        msg_data = loads(request.body)
        new_msg_validator(msg_data)
        print(msg_data)

    except (exc.ValidationError, JSONDecodeError) as err:
        return HttpResponse(dumps({"error": str(err)}))

    return HttpResponse(dumps({"error": None}), status=201)
