import json

import pygame

from src.game.player import Player
from src.server.message_timout import MessageTimeout


class MessageHandler:

    def __init__(self, manual_mode, match_maker):
        self.match_maker = match_maker
        self.event_type = pygame.USEREVENT
        self.timeout = MessageTimeout(manual_mode, self.match_maker.surrender)

    def handle(self, client, message):
        json_message = json.loads(message)
        if not self.match_maker.ready_to_play():
            return self.__handle_init(client, json_message)
        else:
            if self.match_maker.match_paused():
                self.timeout.update_timeout_player(self.match_maker.active_player().player_id)
                return json.dumps({"id": json_message["id"], "gameState": "paused"})

            if self.match_maker.match_over():
                self.timeout.cancel()
                return json.dumps({"id": json_message["id"], "gameState": "finished"})
            else:
                if json_message["type"] == "getState":
                    return self.__handle_get_state(json_message)
                if json_message["type"] == "play":
                    return self.__handle_play(json_message)

    def __handle_init(self, client, json_message):
        if json_message["type"] == "connect":
            return self.__connect_client(client, json_message)
        return json.dumps({"id": json_message["id"], "gameState": "pending"})

    def __connect_client(self, client, json_message):
        self.match_maker.add_player(Player(client["id"], json_message["name"]))
        response = {
            "id": client["id"],
            "connected": True
        }
        if self.match_maker.ready_to_play():
            self.timeout.start()

        return json.dumps(response)

    def __handle_play(self, json_message):
        if json_message["id"] == self.match_maker.active_player().player_id:
            try:
                self.__send_next_move(json.dumps(json_message))
                return json.dumps({"id": json_message["id"], "gameState": "opponent"})
            except pygame.error:
                return json.dumps({"id": json_message["id"], "gameState": "pending"})
        else:
            return json.dumps({"id": json_message["id"], "gameState": "opponent"})

    def __handle_get_state(self, json_message):
        if (self.match_maker.active_player() is not None
                and json_message["id"] == self.match_maker.active_player().player_id):
            player_id = json_message["id"]
            if self.timeout.active_player_has_changed(player_id):
                self.timeout.update_timeout_player(player_id)

            return json.dumps(
                {"id": json_message["id"], "gameState": "playing", "field": self.match_maker.board_state()})
        else:
            return json.dumps({"id": json_message["id"], "gameState": "opponent"})

    def __send_next_move(self, message):
        pygame.fastevent.post(pygame.event.Event(self.event_type, message=message))
