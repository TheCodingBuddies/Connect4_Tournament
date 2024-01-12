from unittest import TestCase

from gameServer.src.Game.player import Player
from gameServer.src.Statistics.game_statistics import GameStatistics


class TestGameStatistics(TestCase):
    def setUp(self):
        self.statistics = GameStatistics()

    def test_init_statistics(self):
        player = Player(1, "newPlayer")
        self.assertEqual(self.statistics.get_win_ratio(player), 0)
        self.assertEqual(self.statistics.get_total_wins(player), 0)

    def test_update_statistic_on_player1_win(self):
        player = Player(1, "newPlayer")
        self.statistics.update_statistics(player)

        self.assertEqual(self.statistics.get_win_ratio(player), 100)
        self.assertEqual(self.statistics.get_total_wins(player), 1)

    def test_update_statistic_on_several_wins(self):
        player1 = Player(1, "Mr.Player1")
        player2 = Player(2, "Dr.Player2")
        self.statistics.update_statistics(player2)
        self.statistics.update_statistics(player2)
        self.statistics.update_statistics(player1)
        self.statistics.update_statistics(player2)

        self.assertEqual(self.statistics.get_win_ratio(player1), 25)
        self.assertEqual(self.statistics.get_total_wins(player1), 1)
        self.assertEqual(self.statistics.get_win_ratio(player2), 75)
        self.assertEqual(self.statistics.get_total_wins(player2), 3)

    def test_get_winner(self):
        player1 = Player(1, "Mr.Player1")
        player2 = Player(2, "Dr.Player2")
        self.statistics.update_statistics(player2)
        self.statistics.update_statistics(player2)
        self.statistics.update_statistics(player1)

        self.assertEqual(self.statistics.get_winner().get_name(), player2.get_name())

    def test_get_no_winner_on(self):
        player1 = Player(1, "Mr.Player1")
        player2 = Player(2, "Dr.Player2")
        self.statistics.update_statistics(player2)
        self.statistics.update_statistics(player1)

        self.assertEqual(self.statistics.get_winner(), None)
