import pyfoobeef
from asyncio import create_task
from json import dumps


def send_foobar2k_updates(state, ws_connections):
    output = {"playback_state": state.playback_state}
    if state.active_item.has_columns():
        col = state.active_item.columns
        output["artist"] = col.artist
        output["title"] = col.title
        output["length"] = col.length
        output["playback_position"] = state.active_item.position_mmss()
    print(output)
    for connection in ws_connections:
        connection.send_msg(dumps(output))


async def foobar2k_event_handler(ws_connections):
    listener = pyfoobeef.EventListener(
        base_url="localhost",
        port=6980,
        active_item_column_map={
            "%artist%": "artist",
            "%title%": "title",
            "%length%": "length",
        },
    )

    def got_update(state):
        send_foobar2k_updates(state, ws_connections)

    # Add callback for player events.
    listener.add_callback("player_state", got_update)

    # Start listening for events from the player.
    await listener.connect(reconnect_time=1)

    # await listener.disconnect()


def start_listener(ws_connections):
    create_task(foobar2k_event_handler(ws_connections))
