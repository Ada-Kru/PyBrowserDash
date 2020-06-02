from datetime import datetime, timezone
from .all_message_types import ALL_MSG_TYPES, DEFAULT_SEEN
from .message_types import MESSAGE_TYPES


def clean_message(msg):
    """
    Format message data.

    Modifies input dictionary in place.
    """
    if "type" not in msg:
        msg["type"] = "unknown_type"
    elif msg["type"] not in ALL_MSG_TYPES:
        msg["type"] = "unknown_type"

    msg.update(ALL_MSG_TYPES[msg["type"]])
    if msg["alert_type"] == MESSAGE_TYPES["log_only"]:
        msg["seen"] = True
        msg["tts"] = False

    if "tts" not in msg:
        msg["tts"] = True

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
