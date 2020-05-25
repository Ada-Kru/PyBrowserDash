import pyfoobeef
from json import dumps


class foobar2k_event_listener():
    """Listen for events from Foobar2000 and send updates to clients."""

    def __init__(self, ws_connections):
        self._listener = None
        self._current_state = None
        self._ws_connections = ws_connections

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
                "%title%": "title",
                "%length%": "length",
            },
        )

        # Add callback for player events.
        self._listener.add_callback("player_state", self.state_changed)

        # Start listening for events from the player.
        await self._listener.connect(reconnect_time=1)

    def state_changed(self, state):
        """Update the current player state and all clients."""
        self._current_state = state
        try:
            self.update_all_clients()
        except Exception as err:
            print(err)

    def update_all_clients(self):
        """Send updates to clients."""
        print("here")
        if self._current_state is not None:
            for connection in self._ws_connections:
                connection.send_msg(self.make_update_str())

    def make_update_str(self):
        """Make a JSON string for websocket updates."""
        if self._current_state is None:
            return '{"playback_state": "disconnected"}'
        state = self._current_state
        output = {"playback_state": state.playback_state}
        if state.active_item.has_columns():
            col = state.active_item.columns
            output["artist"] = col.artist
            output["title"] = col.title
            output["length"] = col.length
            output["playback_position"] = state.active_item.position_mmss()

        print(output)
        return dumps({"music_player": output})

    async def disconnect(self):
        """Disconnect listener."""
        if self._listener is not None:
            await self._listener.disconnect()
            self._listener = None
            self._current_state = None
