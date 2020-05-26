from validx import Dict, Str, Date


new_msg_validator = Dict(
    {
        "from": Str(minlen=1, maxlen=32),
        "message": Str(minlen=1, maxlen=2048),
        "type": Str(),
        "time": Date(nullable=True),
        "data": Str(minlen=1, maxlen=5120),
    },
    defaults={"type": "default", "time": None},
    optional=["data"],
)
