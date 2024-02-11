import json
from unittest import TestCase
from unittest.mock import Mock, patch

import numpy as np
import pygame

from src.game.player import Player
from src.server.message_handler import MessageHandler
from src.tournament.match_maker import MatchMaker


class TestMessageHandler(TestCase):

    def setUp(self):
        pygame.init()
        pygame.fastevent.init()
        self.mocked_match_maker = Mock(spec=MatchMaker)
        self.message_handler = MessageHandler(False, self.mocked_match_maker)

    def test_add_player_on_connect_message(self):
        self.mocked_match_maker.ready_to_play.return_value = False
        client_message = json.dumps({"type": "connect", "name": "player_1"})

        response = json.loads(self.message_handler.handle({"id": 1}, client_message))
        self.mocked_match_maker.add_player.assert_called_once()
        called_player = self.mocked_match_maker.add_player.call_args[0]

        self.assertEqual(called_player[0].name, "player_1")
        self.assertEqual(called_player[0].player_id, 1)
        self.assertEqual(response["connected"], True)
        self.assertEqual(response["id"], 1)

    def test_no_add_player_on_different_message(self):
        self.mocked_match_maker.ready_to_play.return_value = False
        client_message = json.dumps({"type": "play", "id": 1, "name": "player_1"})

        response = json.loads(self.message_handler.handle({"id": 1}, client_message))
        self.mocked_match_maker.add_player.assert_not_called()

        self.assertEqual(response["id"], 1)
        self.assertEqual(response["gameState"], "pending")

    def test_response_opponent_gamestate_on_inactive_player_getState_request(self):
        self.mocked_match_maker.ready_to_play.return_value = True
        self.mocked_match_maker.match_over.return_value = False
        self.mocked_match_maker.active_player.return_value = Player(2, "player_2")
        client_message = json.dumps({"type": "getState", "id": 1, "name": "player_1"})

        response = json.loads(self.message_handler.handle({"id": 1}, client_message))

        self.assertEqual(response["id"], 1)
        self.assertEqual(response["gameState"], "opponent")

    def test_response_playing_gamestate_on_active_player_getState_request(self):
        self.mocked_match_maker.ready_to_play.return_value = True
        self.mocked_match_maker.match_over.return_value = False
        self.mocked_match_maker.active_player.return_value = Player(1, "player_1")
        self.mocked_match_maker.board_state.return_value = np.zeros((2, 2)).tolist()
        client_message = json.dumps({"type": "getState", "id": 1, "name": "player_1"})

        response = json.loads(self.message_handler.handle({"id": 1}, client_message))

        self.assertEqual(response["id"], 1)
        self.assertEqual(response["gameState"], "playing")
        self.assertEqual(response["field"], np.zeros((2, 2)).tolist())

    def test_response_opponent_gamestate_on_inactive_play_request(self):
        self.mocked_match_maker.ready_to_play.return_value = True
        self.mocked_match_maker.match_over.return_value = False
        self.mocked_match_maker.active_player.return_value = Player(2, "player_2")
        client_message = json.dumps({"type": "play", "id": 1, "column": "2"})

        response = json.loads(self.message_handler.handle({"id": 1}, client_message))

        self.assertEqual(response["id"], 1)
        self.assertEqual(response["gameState"], "opponent")

    @patch('pygame.fastevent.post')
    def test_response_opponent_gamestate_on_active_play_request_and_make_turn(self, mocked_fastevent_post):
        self.mocked_match_maker.ready_to_play.return_value = True
        self.mocked_match_maker.match_over.return_value = False
        self.mocked_match_maker.active_player.return_value = Player(1, "player_1")
        client_message = json.dumps({"type": "play", "id": 1, "column": "2"})

        response = json.loads(self.message_handler.handle({"id": 1}, client_message))

        mocked_fastevent_post.assert_called_once_with(pygame.event.Event(pygame.USEREVENT, message=client_message))
        self.assertEqual(response["id"], 1)
        self.assertEqual(response["gameState"], "opponent")

    def test_reset_timeout_on_player_change(self):
        self.mocked_match_maker.ready_to_play.return_value = True
        self.mocked_match_maker.match_over.return_value = False
        self.mocked_match_maker.active_player.return_value = Player(1, "player_1")
        self.mocked_match_maker.board_state.return_value = np.zeros((2, 2)).tolist()
        client_message = json.dumps({"type": "getState", "id": 1, "name": "player_1"})

        self.message_handler.timeout = Mock()
        self.message_handler.timeout.active_player_has_changed.return_value = True

        response = json.loads(self.message_handler.handle({"id": 1}, client_message))

        self.message_handler.timeout.update_timeout_player.assert_called_once()

    def test_keep_timeout_on_player_change(self):
        self.mocked_match_maker.ready_to_play.return_value = True
        self.mocked_match_maker.match_over.return_value = False
        self.mocked_match_maker.active_player.return_value = Player(1, "player_1")
        self.mocked_match_maker.board_state.return_value = np.zeros((2, 2)).tolist()
        client_message = json.dumps({"type": "getState", "id": 1, "name": "player_1"})

        self.message_handler.timeout = Mock()
        self.message_handler.timeout.active_player_has_changed.return_value = False

        response = json.loads(self.message_handler.handle({"id": 1}, client_message))

        self.message_handler.timeout.update_timeout_player.assert_not_called()
