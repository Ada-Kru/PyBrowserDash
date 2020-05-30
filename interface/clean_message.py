from datetime import datetime, timezone
from .all_message_types import ALL_MSG_TYPES, DEFAULT_SEEN


def clean_message(msg):
    """
    Additional formatting of message data.

    Modifies input dictionary in place.
    """
    if msg["type"] not in ALL_MSG_TYPES:
        msg["type"] = "default"

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
        msg["seen"] = False if msg["type"] not in DEFAULT_SEEN else True
