from asyncio import create_task, sleep, CancelledError
from aiohttp import ClientSession

endpoint = "https://api.weather.gov/stations/KDFW/observations/latest?require_qc=false"


class WeatherChecker:
    """Get current weather information for display on frontend."""

    def __init__(self, bg_tasks):
        self._checker = None
        self.current_weather = None
        self._bg_tasks = bg_tasks

    async def start(self):
        """Start checking for weather info from weather.gov."""
        self._checker = create_task(self._get_weather_loop())

    async def _checker_loop(self):
        try:
            headers = {
                "User-Agent": "PyBrowserDash - Local",
                "Content-Type": "application/json",
            }
            async with ClientSession(headers=headers) as session:
                async with session.get(endpoint) as resp:
                    self._update_data(await resp.json())
                    self._update_clients()
                await sleep(60 * 30)
        except CancelledError:
            self._checker = None
            self.current_weather = None
            return

    def _update_data(self, data):
        p = data["properties"]
        weather = {
            "temp": int((9 / 5) * p["temperature"]["value"] + 32),
            "wind_dir": degrees_to_direction(p["windDirection"]["value"]),
            "wind_speed": int(p["windSpeed"]["value"] * 2.236936),
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
        return {
            "weather": {
                "display": f"{cw['temp']}°F {cw['desc']}",
                "hover": f"Wind: {cw['wind_speed']}Mph {cw['wind_dir']}",
            }
        }

    def _update_clients(self):
        """Update clients with new weather information."""
        self._bg_tasks.send_all_websockets(self.make_update())

    async def disconnect(self):
        """Disconnect listener."""
        if self._checker is not None:
            await self._checker.cancel()


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
