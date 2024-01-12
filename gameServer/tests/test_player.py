from unittest import TestCase

from gameServer.src.Game.player import Player


class TestPlayer(TestCase):

    def setUp(self):
        self.player = Player(1, "Hugo")

    def test_get_name(self):
        self.assertEqual(self.player.get_name(), "Hugo")

    def test_get_id(self):
        self.assertEqual(self.player.get_id(), 1)

    def test_get_wins_initially(self):
        self.assertEqual(self.player.get_wins(), 0)

    def test_mark_win_for_player(self):
        self.player.mark_win()

        self.assertEqual(self.player.get_wins(), 1)
