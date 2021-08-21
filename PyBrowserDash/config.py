# User modifiable configuration file
from interface.message_types import MESSAGE_TYPES


# Define custom message types in this dictionary.
# Allowed characters for keys and values are: a-z, A-Z, and _.
custom_message_info = {
    "example_message_type": {
        "alert_type": MESSAGE_TYPES["normal"],
        "class_name": "exampleClassName",
    }
}

# Console command to run for wake on LAN
WOL_COMMAND = r""
# COM port and baud for remote control
COM_PORT = "COM3"
COM_BAUD = 9600
# If true use add /static/css/custom.css to the index html
USE_CUSTOM_STYLES = False
# Weather.gov API endpoint
WEATHER_ENDPOINT = (
    "https://api.weather.gov/stations/KDFW/" "observations/latest?require_qc=false"
)
# User agent to use for the weather.gov API
WEATHER_USER_AGENT = "PyBrowserDash"
