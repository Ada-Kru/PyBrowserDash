from asyncio import create_task, sleep, CancelledError
from aiohttp import ClientSession, ClientError
from datetime import datetime

try:
    from PyBrowserDash.local_config import WEATHER_ENDPOINT, WEATHER_USER_AGENT
except ImportError:
    from PyBrowserDash.config import WEATHER_ENDPOINT, WEATHER_USER_AGENT


class WeatherChecker:
    """Get current weather information for display on frontend."""

    def __init__(self, bg_tasks):
        self._checker = None
        self.current_weather = None
        self._bg_tasks = bg_tasks

    async def start(self):
        """Start checking for weather info from weather.gov."""
        self._checker = create_task(self._checker_loop())

    async def _checker_loop(self):
        """Get weather data from the API every X minutes."""
        try:
            headers = {
                "User-Agent": WEATHER_USER_AGENT,
                "Content-Type": "application/json",
            }
            async with ClientSession(headers=headers) as session:
                while True:
                    try:
                        async with session.get(WEATHER_ENDPOINT) as resp:
                            self._update_data(await resp.json())
                            self._update_clients()
                    except ClientError as err:
                        print(err)
                    await sleep(60 * 30)
        except CancelledError:
            self._checker = None
            self.current_weather = None
            return

    def _update_data(self, data):
        """Update last weather state with the data returned from the API."""
        try:
            p = data["properties"]
            temp = p["temperature"]["value"]
            if temp is None:
                return

            weather = {
                "loaded": True,
                "temp": temp,
                "heat": p["heatIndex"]["value"],
                "chill": p["windChill"]["value"],
                "wind_speed": p["windSpeed"]["value"],
                "wind_dir": p["windDirection"]["value"],
                "wind_gust": p["windGust"]["value"],
                "humidity": p["relativeHumidity"]["value"],
                "pressure": p["barometricPressure"]["value"],
                "desc": p["textDescription"],
                "last_update": datetime.now().strftime("%H:%M").lstrip("0"),
            }
            self.current_weather = weather
        except (ValueError, TypeError, Exception) as err:
            print("Error reading values from weather JSON: ", err)
            return

    def make_update(self):
        """Make an dict of strings with the current weather data."""
        if self.current_weather is not None:
            return self.current_weather
        else:
            return {"loaded": False}

        # Convert weather readings to strings.  Handles null readings.
        # v = current reading.
        # cw = self.current_weather
        # v = cw["temp"]
        # temp = "-" if v is None else f"{convert_temp(v)}"
        # v = cw["wind_speed"]
        # wspeed = 0 if v is None else int(v * 2.237)
        # v = cw["wind_dir"]
        # wdir = "" if v is None else f"{degrees_to_direction(v)}"
        # v = cw["wind_gust"]
        # gust = "" if not v else f" Gust: {int(v * 2.237)} Mph "
        # v = cw["heat"]
        # heat = "" if v is None else f"Heat Index: {convert_temp(v)}°F\n"
        # v = cw["chill"]
        # chill = "" if v is None else f"Wind Chill: {convert_temp(v)}°F\n"
        # v = cw["pressure"]
        # press = "" if v is None else f"Pressure: {int(v / 100)} hPa\n"
        # v = cw["humidity"]
        # hum = "" if v is None else f"Humidity: {int(v)}%"
        # return {
        #     "display": f"{temp}°F ▬ {wspeed} Mph{gust} {wdir} ▬ {cw['desc']}",
        #     "tooltip": (
        #         f"Last updated: {cw['last_update']}\n{heat}{chill}{press}{hum}"
        #     ),
        # }

    def _update_clients(self):
        """Update clients with new weather information."""
        self._bg_tasks.send_all_websockets({"weather": self.make_update()})

    async def disconnect(self):
        """Disconnect listener."""
        if self._checker is not None:
            await self._checker.cancel()


def convert_temp(temp):
    """Convert floating point Celcius temperature to integer Farenheit."""
    return int(cel_to_farn(temp))


def cel_to_farn(temp):
    """Convert Celcius to Farenheit."""
    return (9 / 5) * temp + 32


def degrees_to_direction(degrees):
    """Convert a radial degree integer to a compass heading."""
    if degrees is None or degrees < 22.5:
        return "N"
    elif degrees < 67.5:
        return "NE"
    elif degrees < 112.5:
        return "E"
    elif degrees < 157.5:
        return "SE"
    elif degrees < 202.5:
        return "S"
    elif degrees < 247.5:
        return "SW"
    elif degrees < 292.5:
        return "W"
    elif degrees < 337.5:
        return "NW"
    else:
        return "N"
