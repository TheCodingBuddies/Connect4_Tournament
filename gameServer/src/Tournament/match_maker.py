import pygame

from Game.game import Game
from Game.game_config import GameConfig
from Game.player import Player
from Renderer.renderer import Renderer
from Statistics.game_statistics import GameStatistics


# from . import GameStatistics
# from . import Player


class MatchMaker:

    def __init__(self, rounds, speed_ms):
        self.rounds_left = rounds
        self.speed_ms = speed_ms
        self.statistics = GameStatistics()
        self.active_game = None
        self.renderer = None
        self.surrendered = False
        self.survivor = None

    def start_match(self, player_1: Player, player_2: Player):
        row_amount = 6
        column_amount = 7
        config = GameConfig(row_amount, column_amount, self.speed_ms, player_1, player_2)
        self.renderer = Renderer(120, config.get_columns(), config.get_rows(),
                                 player_1, player_2)
        while self.rounds_left > 0:
            player1_starts = self.rounds_left % 2 == 0
            self.active_game = Game(config, player1_starts, self.renderer)
            winner = self.active_game.play() if not self.surrendered else self.survivor
            self.rounds_left -= 1
            self.statistics.update_statistics(winner)
        self.show_summary()

    def show_summary(self):
        self.renderer.draw_summary(self.statistics)
        manual_quit = False
        while not manual_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    manual_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.renderer.has_user_quit_game(event):
                        manual_quit = True

    def active_player(self):
        return self.active_game.get_active_player()

    def board_state(self):
        return self.active_game.get_board_state().tolist()

    def match_over(self):
        return self.rounds_left <= 0

    def surrender(self):
        self.surrendered = True
        self.survivor = self.active_game.get_inactive_player()
        self.active_game.cancel(self.survivor)
