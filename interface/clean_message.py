from datetime import datetime, timezone
from .all_message_types import ALL_MSG_TYPES, DEFAULT_SEEN
from .message_types import LOG_ONLY_MESSAGE


def clean_message(msg):
    """
    Additional formatting of message data.

    Modifies input dictionary in place.
    """
    if "type" not in msg:
        msg["type"] = "unknown_type"
    elif msg["type"] not in ALL_MSG_TYPES:
        msg["type"] = "unknown_type"

    msg.update(ALL_MSG_TYPES[msg["type"]])
    if msg["alert_type"] == LOG_ONLY_MESSAGE:
        msg["seen"] = True

    if "time" not in msg or msg["time"] is None:
        now = datetime.utcnow()
        msg["time"] = now.replace(
            microsecond=0, tzinfo=timezone.utc
        ).isoformat()

    if "data" not in msg:
        msg["data"] = ""

    if "speech_override" not in msg:
        msg["speech_override"] = None

    if "seen" not in msg:
        msg["seen"] = True if msg["type"] in DEFAULT_SEEN else False
