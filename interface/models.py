from django.db import models


class Message(models.Model):
    """Model for messages."""

    msg_sender = models.CharField(max_length=64)
    msg_text = models.CharField(max_length=2048)
    msg_type = models.CharField(max_length=32)
    msg_time = models.DateTimeField("received at time")
    msg_data = models.CharField(max_length=5120)

    def __str__(self):
        return self.msg_text
