import asyncio
import json
import sys
import time

import websockets

manual_name = "human"


async def connect_to_game(client_id, connected, websocket):
    await websocket.send(json.dumps({"type": "connect", "name": manual_name}))
    connect_string = await websocket.recv()
    connect_obj = json.loads(connect_string)
    if connect_obj["connected"]:
        client_id = connect_obj["id"]
        connected = True
    return client_id, connected


async def get_game_state(client_id, websocket):
    await websocket.send(json.dumps({"id": client_id, "type": "getState"}))
    ask_string = await websocket.recv()
    ask_obj = json.loads(ask_string)
    return ask_obj


async def client():
    uri = "ws://localhost:" + str(port)
    async with websockets.connect(uri) as websocket:
        connected = False
        client_id = 0
        while True:
            if not connected:
                client_id, connected = await connect_to_game(client_id, connected, websocket)
            else:
                state_obj = await get_game_state(client_id, websocket)
                if state_obj["id"] == client_id:
                    match state_obj["gameState"]:
                        case "pending":
                            time.sleep(0.1)
                        case "finished":
                            print("Spiel vorbei. Client wird beendet")
                            return  # oder break?
                        case "playing":
                            print("Enter Column 1-6")
                            column = int(input()) - 1
                            await websocket.send(json.dumps(
                                {
                                    "id": client_id,
                                    "type": "play",
                                    "column": column
                                }
                            ))
                            play_response = await websocket.recv()
                            play_response_obj = json.loads(play_response)
                            if play_response_obj["gameState"] == "finished":
                                return
                        case _:
                            print("Not your turn")
                            time.sleep(0.05)


if __name__ == "__main__":
    port = 8765
    if len(sys.argv) == 2:
        manual_name = sys.argv[1]
    elif len(sys.argv) == 3:
        manual_name = sys.argv[1]
        port = sys.argv[2]
    asyncio.get_event_loop().run_until_complete(client())
