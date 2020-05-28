from django.db import models


class Message(models.Model):
    """Model for messages."""

    sender = models.CharField(max_length=64)
    text = models.CharField(max_length=2048)
    type = models.CharField(max_length=32)
    time = models.DateTimeField("received at time")
    data = models.CharField(max_length=5120, blank=True)

    def __str__(self):
        return f"{self.sender}: {self.text}"
