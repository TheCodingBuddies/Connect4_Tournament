import json
import threading
import time

import pygame

from src.game.player import Player
from src.tournament.match_maker import MatchMaker


class MessageHandler:
    PLAYER_CHECK_TIMEOUT_INTERVAL_IN_S = 0.1

    def __init__(self, manual_mode):
        self.match_maker = MatchMaker(10, 0)
        self.connections = []
        self.event_type = pygame.USEREVENT
        self.timer = threading.Timer(self.PLAYER_CHECK_TIMEOUT_INTERVAL_IN_S, self.__handle_timeout)
        self.timeout_player_id = 0
        self.start_turn_timestamp = 0
        self.player_max_turn_time_in_ms = 2000 if not manual_mode else 20000000

    def handle(self, client, message):
        json_message = json.loads(message)
        if len(self.connections) < 2:
            return self.init_game(client, json_message)
        else:
            if self.match_maker.match_over():
                self.timer.cancel()
                return json.dumps({"id": json_message["id"], "gameState": "finished"})
            else:
                if json_message["type"] == "getState":
                    return self.handle_get_state(json_message)
                if json_message["type"] == "play":
                    return self.handle_play(json_message)

    def init_game(self, client, json_message):
        if json_message["type"] == "connect":
            return self.connect_client(client, json_message)
        return json.dumps({"id": json_message["id"], "gameState": "pending"})

    def connect_client(self, client, json_message):
        self.connections.append((client["id"], json_message["name"]))
        response = {
            "id": client["id"],
            "connected": True
        }
        if self.get_player_count() >= 2:
            self.timer.start()

        return json.dumps(response)

    def handle_play(self, json_message):
        if json_message["id"] == self.match_maker.active_player().player_id:
            try:
                self.send_next_move(json.dumps(json_message))
                return json.dumps({"id": json_message["id"], "gameState": "opponent"})
            except pygame.error:
                return json.dumps({"id": json_message["id"], "gameState": "pending"})
        else:
            return json.dumps({"id": json_message["id"], "gameState": "opponent"})

    def handle_get_state(self, json_message):
        if self.match_maker.active_player() is not None and json_message["id"] == self.match_maker.active_player().player_id:
            if self.timeout_player_id != json_message["id"]:
                self.timeout_player_id = json_message["id"]
                self.start_turn_timestamp = time.process_time_ns()

            return json.dumps(
                {"id": json_message["id"], "gameState": "playing", "field": self.match_maker.board_state()})
        else:
            return json.dumps({"id": json_message["id"], "gameState": "opponent"})

    def send_next_move(self, message):
        pygame.fastevent.post(pygame.event.Event(self.event_type, message=message))

    def start_match(self):
        print(self.connections)
        self.match_maker.start_match(Player(self.connections[0][0], self.connections[0][1]),
                                     Player(self.connections[1][0], self.connections[1][1]))

    def __handle_timeout(self):
        if self.timeout_player_id != 0:
            toc = time.process_time_ns()
            elapsed_in_ms = (toc - self.start_turn_timestamp) // 1000000
            if elapsed_in_ms >= self.player_max_turn_time_in_ms:
                print("timeout for ID:", self.timeout_player_id)
                self.match_maker.surrender()
                return

        self.timer = threading.Timer(self.PLAYER_CHECK_TIMEOUT_INTERVAL_IN_S, self.__handle_timeout)
        self.timer.start()

    def get_player_count(self):
        return len(self.connections)
