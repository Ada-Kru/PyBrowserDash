from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # print(request.scope)
    for connection in request.scope["ws_connections"]:
        connection.send_msg("testin")
    return HttpResponse("...")
