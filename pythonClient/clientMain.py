import asyncio
import json
import sys
import time

import websockets

from Bots.aiFactory import AiFactory
from Bots.bot_ai import BotAI


async def connect_to_game(websocket, bot):
    await websocket.send(json.dumps({"type": "connect", "name": bot.get_name()}))
    connect_string = await websocket.recv()
    connect_obj = json.loads(connect_string)
    if connect_obj["connected"]:
        return connect_obj["id"], True
    else:
        return 0, False


async def get_game_state(websocket, bot):
    await websocket.send(json.dumps({"id": bot.get_player_id(), "type": "getState"}))
    ask_string = await websocket.recv()
    ask_obj = json.loads(ask_string)
    return ask_obj


async def client(bot: BotAI):
    uri = "ws://localhost:" + str(port)
    async with websockets.connect(uri) as websocket:
        connected = False
        while True:
            if not connected:
                client_id, connected = await connect_to_game(websocket, bot)
                bot.set_player_id(client_id)
            else:
                state_obj = await get_game_state(websocket, bot)
                if state_obj["id"] == bot.get_player_id():
                    match state_obj["gameState"]:
                        case "pending":
                            time.sleep(0.1)
                        case "finished":
                            print("Spiel vorbei. Client wird beendet")
                            return  # oder break?
                        case "playing":
                            # time.sleep(1)
                            current_field = state_obj["field"]
                            next_turn = bot.play(current_field)
                            await websocket.send(json.dumps(
                                {
                                    "id": bot.get_player_id(),
                                    "type": "play",
                                    "column": next_turn
                                }
                            ))
                            play_response = await websocket.recv()
                            play_response_obj = json.loads(play_response)
                            if play_response_obj["gameState"] == "finished":
                                return
                        case _:
                            time.sleep(0.05)


if __name__ == "__main__":
    ai_bot = None
    port = 8765
    if len(sys.argv) == 2:
        ai_bot = AiFactory(sys.argv[1])
    elif len(sys.argv) == 3:
        ai_bot = AiFactory(sys.argv[1])
        port = sys.argv[2]
    else:
        ai_bot = AiFactory()
    asyncio.get_event_loop().run_until_complete(client(ai_bot))
