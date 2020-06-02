from validx import Dict, List, Str, Datetime, Bool
from django.utils.dateparse import parse_datetime
from datetime import timezone


new_msg_validator = Dict(
    {
        "sender": Str(minlen=1, maxlen=64),
        "text": Str(minlen=1, maxlen=2048),
        "type": Str(minlen=1, maxlen=32),
        "time": Datetime(
            nullable=True, parser=parse_datetime, tz=timezone.utc
        ),
        "tts": Bool(),
        "data": Str(minlen=0, maxlen=5120),
        "speech_override": Str(nullable=True, minlen=1, maxlen=2048),
        "seen": Bool(),
    },
    defaults={
        "type": "default",
        "time": None,
        "tts": True,
        "seen": False,
        "data": "",
        "speech_override": None,
    },
)

seen_messages_validator = List(Str(minlen=1, maxlen=32))
