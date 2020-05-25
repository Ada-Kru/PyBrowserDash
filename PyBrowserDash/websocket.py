from asyncio import Queue, create_task, as_completed, CancelledError


async def websocket_app(scope, receive, send):
    ws_connections = scope["ws_connections"]
    connection = ws_connection(scope, receive, send)
    ws_connections.add(connection)
    await connection.listen()
    ws_connections.discard(connection)


class ws_connection:
    """Represents an instance of a websocket connection."""

    def __init__(self, scope, receive, send):
        self.connected = False
        self.scope = scope
        self.receive = receive
        self.send = send
        self.q = Queue()

    async def listen(self):
        """Check the message q and handle websocket events until disconnect."""
        q_task = create_task(self.check_queue())
        evt_task = create_task(self.handle_events())
        for fut in as_completed([q_task, evt_task]):
            await fut
            q_task.cancel()

    async def check_queue(self):
        """Check the queue for outgoing messages and send them."""
        try:
            while True:
                msg = await self.q.get()
                await self.send({"type": "websocket.send", "text": msg})
        except CancelledError:
            return

    async def handle_events(self):
        """Handle websocket messages and events."""
        while True:
            evt = await self.receive()
            evt_type = evt["type"]

            if evt_type == "websocket.receive":
                if evt["text"] == "ping":
                    await self.send({"type": "websocket.send", "text": "pong"})
            elif evt_type == "websocket.connect":
                await self.send(
                    {"type": "websocket.accept", "status_code": 101}
                )
                self.connected = True
            elif evt_type == "websocket.disconnect":
                self.connected = False
                break

    def send_msg(self, msg):
        """Send a message over the websocket."""
        if self.connected:
            self.q.put_nowait(msg)
            return True
        else:
            return False
