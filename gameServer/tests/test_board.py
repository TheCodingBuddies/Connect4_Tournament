from unittest import TestCase

import numpy as np

from src.game.board import Board


class TestBoard(TestCase):

    def setUp(self):
        self.board = Board(5, 6)

    def test_get_row_amount(self):
        self.assertEqual(self.board.get_row_amount(), 5)

    def test_get_column_amount(self):
        self.assertEqual(self.board.get_columns_amount(), 6)

    def test_initial_board(self):
        initial_field = np.zeros((5, 6))
        np.testing.assert_array_equal(self.board.get_field(), initial_field)

    def test_is_invalid_location_on_wrong_columns(self):
        invalid_col_list = [-1, 6]
        for col in invalid_col_list:
            with self.subTest(col):
                self.assertEqual(self.board.is_valid_location(col), False)

    def test_is_invalid_location_on_full_column(self):
        for x in range(5):
            self.board.get_field()[x, 0] = 1

        self.assertEqual(self.board.is_valid_location(0), False)

    def test_is_valid_location_on_free_column(self):
        test_field = np.zeros((5, 6))
        test_field[0, 0] = 1
        self.assertEqual(self.board.is_valid_location(0), True)

    def test_update_board_successful_two_turns(self):
        test_field = np.zeros((5, 6))
        test_field[0, 0] = 1
        test_field[1, 0] = 1

        self.board.update_board(0, 1)
        self.board.update_board(0, 1)
        np.testing.assert_array_equal(self.board.get_field(), test_field)
