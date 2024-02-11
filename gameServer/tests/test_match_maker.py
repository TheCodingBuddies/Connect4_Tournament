from unittest import TestCase
from unittest.mock import Mock, patch

import pygame

from src.game.player import Player
from src.tournament.match_maker import MatchMaker


class TestMatchMaker(TestCase):
    def setUp(self):
        self.match_maker = MatchMaker(4, 0)

    def test_init_match_maker(self):
        self.assertEqual(self.match_maker.match_over(), False)

    def test_set_survivor_on_surrender(self):
        mocked_active_game = Mock()
        mocked_active_game.get_inactive_player.return_value = Player(1, "player_1")
        self.match_maker.active_game = mocked_active_game

        self.match_maker.surrender()
        self.assertEqual(self.match_maker.survivor.player_id, 1)
        self.assertEqual(self.match_maker.survivor.name, "player_1")
        mocked_active_game.cancel.assert_called_once_with(self.match_maker.survivor)

    def test_cancel_match_when_not_enough_player(self):
        self.match_maker.start_match()
        self.assertEqual(self.match_maker.active_game, None)

    @patch('src.game.game.Game.play')
    def test_show_summary_after_game(self, mocked_summary):
        self.match_maker.show_summary = Mock()
        self.match_maker.statistics.update_statistics = Mock()
        self.match_maker.players = [Player(1, "player_1"), Player(2, "player_2")]
        self.match_maker.start_match()

        self.match_maker.statistics.update_statistics.assert_called()
        self.match_maker.show_summary.assert_called_once()

    @patch('pygame.event.get')
    def test_draw_summary_on_show(self, mocked_event_get):
        mocked_event_get.return_value = [pygame.event.Event(pygame.QUIT, message="")]
        mocked_renderer = Mock()
        self.match_maker.renderer = mocked_renderer
        self.match_maker.show_summary()

        mocked_renderer.draw_summary.assert_called_once()
