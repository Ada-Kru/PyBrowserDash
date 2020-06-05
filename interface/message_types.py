# Default message types and HTML class names.

MESSAGE_TYPES = {
    "normal": 0,
    "unknown": 1,
    "log_only": 2,
    "delayed_repeat": 3,
    "sensitive": 4,
    "speak_only": 5,
}

message_info = {
    "default": {
        "alert_type": MESSAGE_TYPES["normal"],
        "class_name": "normalMessage",
    },
    "unknown_type": {
        "alert_type": MESSAGE_TYPES["unknown"],
        "class_name": "unknownTypeMessage",
    },
    "log_only": {
        "alert_type": MESSAGE_TYPES["log_only"],
        "class_name": "logOnlyMessage",
    },
    "delayed_repeat": {
        "alert_type": MESSAGE_TYPES["delayed_repeat"],
        "class_name": "delayedRepeatMessage",
    },
    "sensitive": {
        "alert_type": MESSAGE_TYPES["sensitive"],
        "class_name": "sensitiveMessage",
    },
    "speak_only": {
        "alert_type": MESSAGE_TYPES["speak_only"],
        "class_name": "speakOnlyMessage",
    },
}
