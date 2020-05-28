NORMAL_MESSAGE = 0
LOG_ONLY_MESSAGE = 1
DELAYED_REPEAT_MESSAGE = 2
UNKNOWN_TYPE_MESSAGE = 3

message_types = {
    "default": {"alert_type": NORMAL_MESSAGE, "class_name": "normalMessage"},
    "log_only": {
        "alert_type": LOG_ONLY_MESSAGE,
        "class_name": "logOnlyMessage",
    },
    "delayed_repeat": {
        "alert_type": DELAYED_REPEAT_MESSAGE,
        "class_name": "delayedRepeatMessage",
    },
    "unknown_type": {
        "alert_type": UNKNOWN_TYPE_MESSAGE,
        "class_name": "unknownTypeMessage",
    },
}
