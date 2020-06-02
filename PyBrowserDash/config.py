from interface.message_types import (
    NORMAL_MESSAGE,
    LOG_ONLY_MESSAGE,
    DELAYED_REPEAT_MESSAGE,
    UNKNOWN_TYPE_MESSAGE,
)


# Define custom message types in this dictionary.
# Allowed characters for keys and values are: a-z, A-Z, and _.
custom_message_types = {
    "example_message_type": {
        "alert_type": NORMAL_MESSAGE,
        "class_name": "exampleClassName",
    }
}

# Console command to run for wake on LAN
WOL_COMMAND = r""
# If true use add /static/css/custom.css to the index html
USE_CUSTOM_STYLES = False
