from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("messages/new/", views.messages_new, name="messages_new"),
    path("messages/unseen/", views.messages_unseen, name="messages_unseen"),
    path(
        "messages/clear_unseen/",
        views.messages_clear_unseen,
        name="messages_clear_unseen",
    ),
    path(
        "messages/history/<int:limit>/",
        views.messages_history,
        name="messages_history",
    ),
    path("W/", views.wake_on_lan, name="wake_on_lan"),
]
