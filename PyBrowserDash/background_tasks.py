from PyBrowserDash.music import MusicEventListener
from PyBrowserDash.system_monitor import SystemMonitor
from PyBrowserDash.weather import WeatherChecker
from PyBrowserDash.text_speaker import TextSpeaker
from PyBrowserDash.remote_control import RemoteControl
from asyncio import create_task


class BackgroundTasks:
    """Handle background tasks and allow communication with async functions."""

    def __init__(self):
        self.ws_connections = set()
        self._music_event_listener = MusicEventListener(self)
        self._system_monitor = SystemMonitor(self)
        self._weather_checker = WeatherChecker(self)
        self._tasks_started = False
        self._text_speaker = TextSpeaker()
        self._remote_control = RemoteControl()
        self._muted = False
        self.unseen = {}
        self.no_repeat = {}

    def tasks_started(self):
        """Return if tasks have been started."""
        return self._tasks_started

    async def start_tasks(self):
        """Start background tasks."""
        self._tasks_started = True
        await self._music_event_listener.listen()
        create_task(self._system_monitor.run())
        await self._weather_checker.start()

    def send_all_websockets(self, data):
        """Send message to all clients."""
        for connection in self.ws_connections:
            connection.send_msg(data)

    def speak(self, text):
        """Speak a message out loud."""
        self._text_speaker.speak(text)

    def toggle_mute(self):
        """Toggle muted status."""
        self._muted ^= True

    def is_muted(self):
        """Return if audio is muted."""
        return self._muted

    def send_rc(self, command, emitters):
        """Send a command to the remote control."""
        return self._remote_control.send_cmd(command, emitters)

    def get_backend_status(self):
        """Get a dictionary with the backend's status."""
        return {"backend": {"muted": self._muted}}

    def get_music_player_status(self):
        """Get a dictionary with the audio player's status."""
        return self._music_event_listener.make_update()

    def get_weather_status(self):
        """Get a dictionary with the status for the weather module."""
        return {"weather": self._weather_checker.make_update()}

    def make_initial_status(self):
        """Make a dict of the module statuses for when clients connect."""
        backend = self.get_backend_status()
        music = self.get_music_player_status()
        weather = self.get_weather_status()
        return {"unseen": self.unseen, **music, **weather, **backend}
