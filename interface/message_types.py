NORMAL_MESSAGE = 0
LOG_ONLY_MESSAGE = 1
DELAYED_REPEAT_MESSAGE = 2

message_types = {
    "default": {"alert_type": NORMAL_MESSAGE, "class_name": "normalMessage"},
    "log_only": {
        "alert_type": LOG_ONLY_MESSAGE,
        "class_name": "logOnlyMessage",
    },
    "delated_repeat": {
        "alert_type": DELAYED_REPEAT_MESSAGE,
        "class_name": "delayedRepeatMessage",
    },
}
