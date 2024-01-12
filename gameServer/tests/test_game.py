import json
from unittest import TestCase
from unittest.mock import patch, Mock

import pygame

from gameServer.src.Game.game import Game
from gameServer.src.Game.game_config import GameConfig
from gameServer.src.Game.player import Player


def turn(column, player_id):
    return pygame.event.Event(pygame.USEREVENT, message=json.dumps({"id": player_id, "column": column}))


class TestGame(TestCase):

    def setUp(self):
        pygame.init()
        pygame.fastevent.init()
        self.player_1 = Player(1, "player1")
        self.player_2 = Player(2, "player2")
        config = GameConfig(5, 6, 0, self.player_1, self.player_2)
        renderer = Mock()
        self.game = Game(config, True, renderer)

    @patch('pygame.event.get')
    def test_player_one_wins(self, mocked_event_get):
        mocked_event_get.return_value = [turn(0, 1), turn(1, 2), turn(0, 1), turn(1, 2), turn(0, 1), turn(1, 2),
                                         turn(0, 1)]
        self.game.play()
        self.assertEqual(self.game.get_winner(), self.player_1)

    @patch('pygame.event.get')
    def test_player_two_wins(self, mocked_event_get):
        mocked_event_get.return_value = [turn(0, 1), turn(1, 2), turn(0, 1), turn(1, 2), turn(0, 1), turn(1, 2),
                                         turn(2, 1), turn(1, 2)]
        self.game.play()
        self.assertEqual(self.game.get_winner(), self.player_2)

    @patch('pygame.event.get')
    def test_player_one_wins_because_of_invalid_opponent_turn(self, mocked_event_get):
        mocked_event_get.return_value = [turn(0, 1), turn(0, 2), turn(0, 1), turn(0, 2), turn(0, 1), turn(0, 2)]
        self.game.play()
        self.assertEqual(self.game.get_winner(), self.player_1)

    @patch('pygame.event.get')
    def test_player_one_loose_because_choosing_invalid_col(self, mocked_event_get):
        mocked_event_get.return_value = [turn(8, 1)]
        self.game.play()
        self.assertEqual(self.game.get_winner(), self.player_2)

    @patch('pygame.event.get')
    def test_player_one_loose_because_no_turn_left(self, mocked_event_get):
        mocked_event_get.return_value = [
            turn(0, 1), turn(1, 2), turn(2, 1), turn(3, 2), turn(4, 1), turn(5, 2),
            turn(5, 1), turn(4, 2), turn(3, 1), turn(2, 2), turn(1, 1), turn(0, 2),
            turn(5, 1), turn(4, 2), turn(3, 1), turn(2, 2), turn(1, 1), turn(0, 2),
            turn(0, 1), turn(1, 2), turn(2, 1), turn(3, 2), turn(4, 1), turn(5, 2),
            turn(0, 1), turn(1, 2), turn(2, 1), turn(3, 2), turn(4, 1), turn(5, 2),
            turn(0, 1)
        ]
        self.game.play()
        self.assertEqual(self.game.get_winner(), self.player_2)

    def test_player_one_surrenders_and_two_wins(self):
        self.game.cancel(self.player_2)
        self.assertEqual(self.game.get_winner(), self.player_2)
