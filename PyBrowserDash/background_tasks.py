from PyBrowserDash.foobar2k import foobar2k_event_listener
from PyBrowserDash.system_monitor import SystemMonitor
from PyBrowserDash.text_speaker import TextSpeaker
from asyncio import create_task


class BackgroundTasks():
    """Handle asynchronous background tasks and events from views."""

    def __init__(self):
        self.ws_connections = set()
        ael = foobar2k_event_listener(self.ws_connections)
        self._audio_event_listener = ael
        self._system_monitor = SystemMonitor(self)
        self._tasks_started = False
        self._text_speaker = TextSpeaker()
        self._muted = False

    def tasks_started(self):
        """Return if tasks have been started."""
        return self._tasks_started

    async def start_tasks(self):
        """Start background tasks."""
        self._tasks_started = True
        await self._audio_event_listener.listen()
        create_task(self._system_monitor.run())

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

    def get_status(self):
        """Get a dictionary with the backend's status."""
        return {"muted": self._muted}
