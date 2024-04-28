import json
import sys
import time

import numpy as np
import pygame

from ..game.board import Board
from ..game.game_config import GameConfig
from ..game.referee import Referee


class Game:

    def __init__(self, game_config: GameConfig, player1_starts, renderer):
        self.board = Board(game_config.get_rows(), game_config.get_columns())
        self.referee = Referee()
        self.speed_ms = game_config.get_speed()
        self.game_config = game_config
        self.active_player = game_config.get_player_one() if player1_starts else game_config.get_player_two()
        self.inactive_player = game_config.get_player_two() if player1_starts else game_config.get_player_one()
        self.winner = None
        self.renderer = renderer
        self.winner_move = None
        self.invalid_move = None
        self.canceled = False
        self.paused = False

    def get_winner(self):
        return self.winner

    def get_board_state(self):
        return self.board.get_field()

    def get_active_player(self):
        return self.active_player

    def get_inactive_player(self):
        return self.inactive_player

    def play(self):
        self.renderer.init_board(self.board)
        self.renderer.draw_player_names()
        self.renderer.draw_wins_amount()

        while self.referee.keep_playing() and not self.canceled:
            for event in pygame.fastevent.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__adjust_speed(self.renderer.is_speed_button_pressed())

                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type != pygame.USEREVENT:
                    continue

                if self.paused:
                    self.paused = True
                    continue

                if not self.referee.keep_playing():
                    break

                if event.type == pygame.USEREVENT:
                    message = json.loads(event.message)
                    if message["id"] == self.active_player.get_id():
                        self.__iterate_game(message["column"])
                        self.renderer.draw_chips(self.board)
                        if self.winner:
                            self.__draw_finish()
                            time.sleep(1)
                        else:
                            self.__toggle_players()
        self.__print_game_finished()
        return self.winner

    def cancel(self, survivor):
        self.winner = survivor
        self.canceled = True

    def __adjust_speed(self, mode):
        if mode == "Pause":
            self.paused = True
        if mode == "Play":
            self.paused = False
            self.game_config.speed_ms = 500
        if mode == "Faster":
            self.paused = False
            self.game_config.speed_ms = 0

    def __draw_finish(self):
        if self.winner_move:
            self.renderer.draw_winner_move(self.winner_move)
        else:
            self.renderer.draw_invalid_move(self.invalid_move, self.winner)
        self.renderer.hype_winner(self.winner)

    def __iterate_game(self, column):
        valid = self.referee.is_turn_valid(self.board, column)
        pygame.time.wait(self.game_config.speed_ms)
        if valid:
            self.board.update_board(column, self.active_player.get_id())
            self.winner_move = self.referee.check_for_win(self.board, self.active_player.get_id())
            if self.winner_move:
                self.active_player.mark_win()
                self.winner = self.active_player
        else:
            self.invalid_move = column
            self.inactive_player.mark_win()
            self.winner = self.inactive_player

    def __print_game_finished(self):
        print(np.flip(self.board.get_field(), 0))
        print(self.winner.get_name(), "wins")
        print("game finished")

    def __toggle_players(self):
        self.active_player, self.inactive_player = self.inactive_player, self.active_player
