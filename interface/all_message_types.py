try:
    from PyBrowserDash.local_config import custom_message_info
except ImportError:
    from PyBrowserDash.config import custom_message_info
from .message_types import message_info, MESSAGE_TYPES


# Make a dictionary of both default and custom message types.
ALL_MSG_TYPES = {**message_info, **custom_message_info}
# Create a set of all message types that should default to being marked as read
DEFAULT_SEEN = set(
    key
    for key, val in ALL_MSG_TYPES.items()
    if val["alert_type"] == MESSAGE_TYPES["log_only"]
)
