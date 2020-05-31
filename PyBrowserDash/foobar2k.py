import pyfoobeef


class foobar2k_event_listener():
    """Listen for events from Foobar2000 and send updates to clients."""

    def __init__(self, bg_tasks):
        self._listener = None
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
        self.update_all_clients()

    def update_client(self, client):
        """Send player state to a single clent."""
        client.send_msg(self.make_update())

    def update_all_clients(self):
        """Send updates to clients."""
        self._bg_tasks.send_all_websockets(self.make_update())

    def make_update(self):
        """Make a status dictionary for websocket updates."""
        if self._current_state is None:
            return {"music": "disconnected"}

        state = self._current_state
        output = {"music": state.playback_state}
        if state.active_item.has_columns():
            col = state.active_item.columns
            output["artist"] = col.artist
            output["title"] = col.title
            output["length"] = state.active_item.duration
            output["position"] = state.active_item.position

        return {"music": output}

    async def disconnect(self):
        """Disconnect listener."""
        if self._listener is not None:
            await self._listener.disconnect()
            self._listener = None
            self._current_state = None
