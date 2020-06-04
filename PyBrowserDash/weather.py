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
        p = data["properties"]
        humidity = p["relativeHumidity"]["value"]
        humidity = int(humidity) if humidity is not None else 0
        weather = {
            "temp": celcius_to_farenheit(p["temperature"]["value"], True),
            "heat": celcius_to_farenheit(p["heatIndex"]["value"], True),
            "chill": celcius_to_farenheit(p["windChill"]["value"], True),
            "wind_dir": degrees_to_direction(p["windDirection"]["value"]),
            "wind_speed": int(p["windSpeed"]["value"] * 2.237),
            "wind_gust": p["windGust"]["value"],
            "humidity": humidity,
            "desc": p["textDescription"],
        }
        self.current_weather = weather

    def make_update(self):
        """Make an dict of strings with the current weather data."""
        if self.current_weather is None:
            return {
                "display": "Weather info not loaded",
                "hover": "Weather info not loaded",
            }

        cw = self.current_weather
        wind_gust = cw["wind_gust"]
        gust_str = "" if not wind_gust else f"-{wind_gust * 2.237}"
        return {
            "display": (
                f"{cw['temp']}°F ▬▬ {cw['wind_speed']}{gust_str}Mph "
                f"{cw['wind_dir']} ▬▬ {cw['desc']}"
            ),
            "hover": (
                f"Last updated: {datetime.now().strftime('%H:%M')}\n"
                f"Heat Index: {cw['heat']}°F\n"
                f"Wind Chill: {cw['chill']}°F\n"
                f"Humidity: {cw['humidity']}%"
            ),
        }

    def _update_clients(self):
        """Update clients with new weather information."""
        self._bg_tasks.send_all_websockets(self.make_update())

    async def disconnect(self):
        """Disconnect listener."""
        if self._checker is not None:
            await self._checker.cancel()


def celcius_to_farenheit(temp, as_int=False):
    if temp is None:
        return 0
    output = int((9 / 5) * temp + 32)
    return int(output) if as_int else output


def degrees_to_direction(degrees):
    if degrees < 22.5:
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
