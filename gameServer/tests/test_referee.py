from unittest import TestCase

from src.game.board import Board
from src.game.referee import Referee


def win_vertically_board():
    board = Board(5, 6)
    board.get_field()[0][0] = 1
    board.get_field()[1][0] = 1
    board.get_field()[2][0] = 1
    board.get_field()[3][0] = 1
    return board


def win_horizontally_board():
    board = Board(5, 6)
    board.get_field()[0][0] = 1
    board.get_field()[0][1] = 1
    board.get_field()[0][2] = 1
    board.get_field()[0][3] = 1
    return board


def win_ascending_diagonally_board():
    board = Board(5, 6)
    board.get_field()[0][0] = 1
    board.get_field()[1][1] = 1
    board.get_field()[2][2] = 1
    board.get_field()[3][3] = 1
    return board


def win_descending_diagonally_board():
    board = Board(5, 6)
    board.get_field()[3][0] = 1
    board.get_field()[2][1] = 1
    board.get_field()[1][2] = 1
    board.get_field()[0][3] = 1
    return board


class TestReferee(TestCase):

    def setUp(self):
        self.referee = Referee()

    def test_is_turn_valid(self):
        board = Board(5, 6)
        self.assertEqual(self.referee.is_turn_valid(board, 0), True)
        self.assertEqual(self.referee.keep_playing(), True)

    def test_is_turn_invalid(self):
        board = Board(5, 6)
        self.assertEqual(self.referee.is_turn_valid(board, -1), False)
        self.assertEqual(self.referee.keep_playing(), False)

    def test_game_not_over_without_win(self):
        self.assertEqual(self.referee.keep_playing(), True)

    def test_game_over_after_win(self):
        self.referee.check_for_win(win_horizontally_board(), 1)

        self.assertEqual(self.referee.keep_playing(), False)

    def test_no_player_wins_on_initial_board(self):
        board = Board(5, 6)
        self.assertEqual(self.referee.check_for_win(board, 1), None)
        self.assertEqual(self.referee.check_for_win(board, 2), None)

    def test_check_for_win_on_winning_boards(self):
        winning_boards = [win_horizontally_board(), win_vertically_board(), win_ascending_diagonally_board(),
                          win_descending_diagonally_board()]
        wins = [[(0, 0), (0, 1), (0, 2), (0, 3)],
                [(0, 0), (1, 0), (2, 0), (3, 0)],
                [(0, 0), (1, 1), (2, 2), (3, 3)],
                [(3, 0), (2, 1), (1, 2), (0, 3)]]
        i = 0

        for board in winning_boards:
            with self.subTest(board):
                self.assertEqual(self.referee.check_for_win(board, 1), wins[i])
            i += 1
