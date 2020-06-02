MESSAGE_TYPES = {
    "normal": 0,
    "log_only": 1,
    "delayed_repeat": 2,
    "sensitive": 3,
    "unknown": 4,
}

message_info = {
    "default": {
        "alert_type": MESSAGE_TYPES["normal"],
        "class_name": "normalMessage",
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
    "unknown_type": {
        "alert_type": MESSAGE_TYPES["unknown"],
        "class_name": "unknownTypeMessage",
    },
}
