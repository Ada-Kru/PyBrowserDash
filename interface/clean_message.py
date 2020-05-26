from datetime import datetime, timezone
from .message_types import (
    NORMAL_MESSAGE,
    LOG_ONLY_MESSAGE,
    DELAYED_REPEAT_MESSAGE,
    message_types,
)

try:
    from PyBrowserDash.local_config import custom_message_types
except ImportError:
    from PyBrowserDash.config import custom_message_types


ALL_MSG_TYPES = {**message_types, **custom_message_types}


def clean_message(msg):
    """
    Additional formatting of message data.

    Modifies input dictionary in place.
    """
    if msg["time"] is None:
        now = datetime.utcnow()
        msg["time"] = now.replace(
            microsecond=0, tzinfo=timezone.utc
        ).isoformat()

    msg["type"] = ALL_MSG_TYPES.get(msg["type"], ALL_MSG_TYPES["default"])
