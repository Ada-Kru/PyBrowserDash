async def websocket_app(scope, receive, send):
    while True:
        evt = await receive()
        evt_type = evt["type"]

        if evt_type == "websocket.receive":
            if evt["text"] == "ping":
                await send({"type": "websocket.send", "text": "pong"})
        elif evt_type == "websocket.connect":
            await send({"type": "websocket.accept", "status_code": 101})
        elif evt_type == "websocket.disconnect":
            break
