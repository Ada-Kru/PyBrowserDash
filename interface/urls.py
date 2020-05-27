from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("messages/new/", views.messages_new, name="messages_new"),
    path("messages/<int:limit>/", views.messages_get, name="messages_get"),
]
