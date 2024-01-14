import numpy as np


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.field = np.zeros((self.rows, self.columns))

    def is_valid_location(self, col):
        return self.field[self.rows - 1][col] == 0 if 0 <= col < self.columns else False

    def __get_next_open_row(self, col):
        for r in range(self.rows):
            if self.field[r][col] == 0:
                return r

    def update_board(self, col, player_id):
        row = self.__get_next_open_row(col)
        self.field[row][col] = player_id

    def get_columns_amount(self):
        return self.columns

    def get_row_amount(self):
        return self.rows

    def get_field(self):
        return self.field
