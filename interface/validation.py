from validx import Dict, Str, Datetime, Bool
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
        "data": Str(minlen=0, maxlen=5120),
        "seen": Bool(),
    },
    defaults={"type": "default", "time": None, "seen": False, "data": ""},
)
