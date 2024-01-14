import json
import random
import threading
import time

import pygame
import websockets

from ..tournament.match_maker import MatchMaker
from ..game.player import Player


class Server:
    PLAYER_CHECK_TIMEOUT_INTERVAL_IN_S = 0.1
    PLAYER_MAX_TURN_TIME_IN_MS = 2000

    def __init__(self, ip, port, match_maker: MatchMaker):
        self.ip = ip
        self.port = port
        self.event_type = pygame.USEREVENT
        self.connections = []
        self.match_maker = match_maker
        self.timer = threading.Timer(self.PLAYER_CHECK_TIMEOUT_INTERVAL_IN_S, self.__handle_timeout)
        self.timeout_player_id = 0
        self.start_turn_timestamp = 0

    async def handle(self, websocket):
        async for message in websocket:
            json_message = json.loads(message)
            if len(self.connections) < 2:
                await self.init_game(json_message, websocket)
            else:
                if self.match_maker.match_over():
                    await websocket.send(json.dumps({"id": json_message["id"], "gameState": "finished"}))
                else:
                    if json_message["type"] == "getState":
                        await self.handle_get_state(json_message, websocket)
                    if json_message["type"] == "play":
                        await self.handle_play(json_message, websocket)

    async def handle_play(self, json_message, websocket):
        if json_message["id"] == self.match_maker.active_player().player_id:
            try:
                await self.send_next_move(json.dumps(json_message))
                await websocket.send(json.dumps({"id": json_message["id"], "gameState": "opponent"}))
            except pygame.error:
                await websocket.send(json.dumps({"id": json_message["id"], "gameState": "pending"}))
        else:
            await websocket.send(json.dumps({"id": json_message["id"], "gameState": "opponent"}))

    async def handle_get_state(self, json_message, websocket):
        if json_message["id"] == self.match_maker.active_player().player_id:
            if self.timeout_player_id != json_message["id"]:
                self.timeout_player_id = json_message["id"]
                self.start_turn_timestamp = time.process_time_ns()

            await websocket.send(
                json.dumps({"id": json_message["id"], "gameState": "playing", "field": self.match_maker.board_state()})
            )
        else:
            await websocket.send(json.dumps({"id": json_message["id"], "gameState": "opponent"}))

    def __handle_timeout(self):
        if self.timeout_player_id != 0:
            toc = time.process_time_ns()
            elapsed_in_ms = (toc - self.start_turn_timestamp) // 1000000
            if elapsed_in_ms >= self.PLAYER_MAX_TURN_TIME_IN_MS:
                print("timeout for ID:", self.timeout_player_id)
                self.match_maker.surrender()
                return

        self.timer = threading.Timer(self.PLAYER_CHECK_TIMEOUT_INTERVAL_IN_S, self.__handle_timeout)
        self.timer.start()

    async def init_game(self, json_message, websocket):
        if json_message["type"] == "connect":
            await self.connect_client(json_message, websocket)
        else:
            await websocket.send(json.dumps({"id": json_message["id"], "gameState": "pending"}))

    async def connect_client(self, json_message, websocket):
        new_id = random.randint(1, 5000)
        self.connections.append((new_id, json_message["name"]))
        print("add client with id:", new_id)
        response = {
            "id": new_id,
            "connected": True
        }
        print(json.dumps(response))
        await websocket.send(json.dumps(response))
        if self.get_player_count() >= 2:
            self.timer.start()

    async def send_next_move(self, message):
        pygame.fastevent.post(pygame.event.Event(self.event_type, message=message))

    async def main(self, future):
        async with websockets.serve(self.handle, self.ip, self.port):
            await future  # run forever

    def start_server(self, loop, future):
        print("start game server..")
        loop.run_until_complete(self.main(future))

    def stop_server(self, loop, future):
        self.timer.cancel()
        loop.call_soon_threadsafe(future.set_result, None)

    def get_player_count(self):
        return len(self.connections)

    def start_match(self):
        self.match_maker.start_match(Player(self.connections[0][0], self.connections[0][1]),
                                     Player(self.connections[1][0], self.connections[1][1]))
