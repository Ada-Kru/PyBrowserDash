import pyfoobeef
from asyncio import create_task, sleep, CancelledError


class MusicEventListener:
    """Listen for events from Foobar2000 and send updates to clients."""

    def __init__(self, bg_tasks):
        self._listener = None
        self._connection_checker = None
        self._current_state = None
        self._bg_tasks = bg_tasks

    def is_started(self):
        """Return if listener is running or not."""
        return self._listener is not None

    async def listen(self):
        """Start Event Listener."""
        if self.is_started():
            await self.disconnect()
        self._listener = pyfoobeef.EventListener(
            base_url="localhost",
            port=6980,
            active_item_column_map={
                "%artist%": "artist",
                "%album%": "album",
                "%title%": "title",
                "%length%": "length",
            },
        )

        # Add callback for player events.
        self._listener.add_callback("player_state", self.state_changed)

        # Start listening for events from the player.
        await self._listener.connect(reconnect_time=1)
        self._connection_checker = create_task(self._check_connected())

    async def _check_connected(self):
        """Check if the player has disconnected."""
        try:
            while True:
                connected = self._current_state is not None
                if connected and not self._listener.is_connected():
                    self._current_state = None
                    self.update_all_clients()
                await sleep(1)
        except CancelledError:
            return

    def state_changed(self, state):
        """Update the current player state and all clients."""
        self._current_state = state
        self.update_all_clients()

    def update_client(self, client):
        """Send player state to a single clent."""
        client.send_msg(self.make_update())

    def update_all_clients(self):
        """Send updates to clients."""
        self._bg_tasks.send_all_websockets(self.make_update())

    def make_update(self):
        """Make a status dictionary for websocket updates."""
        state = self._current_state
        if state is None:
            return {"music": {"player_state": "disconnected", "active_item": {}}}

        active_info = {}
        if state.active_item.has_columns():
            col = state.active_item.columns
            active_info["artist"] = col.artist
            active_info["album"] = col.album
            active_info["title"] = col.title
            active_info["length"] = state.active_item.duration
            active_info["position"] = state.estimated_position()

        return {
            "music": {
                "player_state": state.playback_state,
                "active_item": active_info,
            }
        }

    async def disconnect(self):
        """Disconnect listener."""
        if self._listener is not None:
            await self._connection_checker.cancel()
            await self._listener.disconnect()
            self._listener = None
            self._current_state = None
