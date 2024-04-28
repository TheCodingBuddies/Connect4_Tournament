import pygame

from ..game.game import Game
from ..game.game_config import GameConfig
from ..renderer.renderer import Renderer
from ..statistics.game_statistics import GameStatistics


class MatchMaker:

    def __init__(self, rounds, speed_ms):
        self.rounds_left = rounds
        self.speed_ms = speed_ms
        self.statistics = GameStatistics()
        self.active_game = None
        self.renderer = None
        self.surrendered = False
        self.survivor = None
        self.players = []

    def add_player(self, player):
        if len(self.players) < 2:
            self.players.append(player)

    def ready_to_play(self):
        return len(self.players) == 2

    def start_match(self):
        if not self.ready_to_play():
            print("Not enough player! Stop game")
            return

        row_amount = 6
        column_amount = 7
        config = GameConfig(row_amount, column_amount, self.speed_ms, self.players[0], self.players[1])
        self.renderer = Renderer(120, config.get_columns(), config.get_rows(),
                                 self.players[0], self.players[1])

        self.show_start_screen(self.rounds_left)
        while self.rounds_left > 0:
            player1_starts = self.rounds_left % 2 == 0
            self.active_game = Game(config, player1_starts, self.renderer)
            winner = self.active_game.play() if not self.surrendered else self.survivor
            self.rounds_left -= 1
            self.statistics.update_statistics(winner)
        self.show_summary()

    def show_start_screen(self, rounds):
        self.renderer.draw_start_screen(rounds)
        self.__wait_for_button_emit()

    def show_summary(self):
        self.renderer.draw_summary(self.statistics)
        self.__wait_for_button_emit()

    def __wait_for_button_emit(self):
        manual_quit = False
        while not manual_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    manual_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.renderer.has_user_emit_button(event):
                        manual_quit = True

    def active_player(self):
        return self.active_game.get_active_player() if self.active_game is not None else None

    def board_state(self):
        return self.active_game.get_board_state().tolist()

    def match_over(self):
        return self.rounds_left <= 0

    def match_paused(self):
        return self.active_game is not None and self.active_game.paused

    def surrender(self):
        self.surrendered = True
        self.survivor = self.active_game.get_inactive_player()
        self.active_game.cancel(self.survivor)
