try:
    from PyBrowserDash.local_config import custom_message_types
except ImportError:
    from PyBrowserDash.config import custom_message_types
from .message_types import message_types, LOG_ONLY_MESSAGE


ALL_MSG_TYPES = {**message_types, **custom_message_types}
DEFAULT_SEEN = set(
    key
    for key, val in ALL_MSG_TYPES.items()
    if val["alert_type"] == LOG_ONLY_MESSAGE
)

WOL_COMMAND = ""
