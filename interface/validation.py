from validx import Dict, Str, Datetime
from django.utils.dateparse import parse_datetime
from datetime import timezone


new_msg_validator = Dict(
    {
        "from": Str(minlen=1, maxlen=64),
        "message": Str(minlen=1, maxlen=2048),
        "type": Str(minlen=1, maxlen=32),
        "time": Datetime(
            nullable=True, parser=parse_datetime, tz=timezone.utc
        ),
        "data": Str(minlen=1, maxlen=5120),
    },
    defaults={"type": "default", "time": None},
    optional=["data"],
)
