from unittest import TestCase

from gameServer.src.Game.game_config import GameConfig
from gameServer.src.Game.player import Player


class TestGameConfig(TestCase):

    def setUp(self):
        self.config = GameConfig(3, 7, 10, Player(1, "Player 1"), Player(2, "Player 2"))

    def test_get_rows(self):
        self.assertEqual(self.config.get_rows(), 3)

    def test_get_columns(self):
        self.assertEqual(self.config.get_columns(), 7)

    def test_get_player_one(self):
        self.assertEqual(self.config.get_player_one().get_name(), "Player 1")

    def test_get_player_two(self):
        self.assertEqual(self.config.get_player_two().get_name(), "Player 2")

    def test_get_speed(self):
        self.assertEqual(self.config.get_speed(), 10)
