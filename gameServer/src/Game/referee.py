from enum import Enum  # for enum34, or the stdlib version


class Result(Enum):
    WIN = 1
    LOOSE = 2
    CONTINUE = 3


class Referee:
    Result = Enum('Result', 'win loose play')

    def __init__(self):
        self.turn = 0
        self.game_over = False

    def keep_playing(self):
        return not self.game_over

    def check_for_win(self, board, player_id):
        # Check horizontal locations for win
        for c in range(board.get_columns_amount() - 3):
            for r in range(board.get_row_amount()):
                if board.get_field()[r][c] == player_id and board.get_field()[r][c + 1] == player_id \
                        and board.get_field()[r][c + 2] == player_id and board.get_field()[r][c + 3] == player_id:
                    self.game_over = True
                    return [(r, c), (r, c + 1), (r, c + 2), (r, c + 3)]

        # Check vertical locations for win
        for c in range(board.get_columns_amount()):
            for r in range(board.get_row_amount() - 3):
                if board.get_field()[r][c] == player_id and board.get_field()[r + 1][c] == player_id \
                        and board.get_field()[r + 2][c] == player_id and board.get_field()[r + 3][c] == player_id:
                    self.game_over = True
                    return [(r, c), (r + 1, c), (r + 2, c), (r + 3, c)]

        # Check positively sloped diaganols
        for c in range(board.get_columns_amount() - 3):
            for r in range(board.get_row_amount() - 3):
                if board.get_field()[r][c] == player_id and board.get_field()[r + 1][c + 1] == player_id \
                        and board.get_field()[r + 2][c + 2] == player_id and board.get_field()[r + 3][
                    c + 3] == player_id:
                    self.game_over = True
                    return [(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)]

        # Check negatively sloped diaganols
        for c in range(board.get_columns_amount() - 3):
            for r in range(3, board.get_row_amount()):
                if board.get_field()[r][c] == player_id and board.get_field()[r - 1][c + 1] == player_id \
                        and board.get_field()[r - 2][c + 2] == player_id and board.get_field()[r - 3][
                    c + 3] == player_id:
                    self.game_over = True
                    return [(r, c), (r - 1, c + 1), (r - 2, c + 2), (r - 3, c + 3)]

        return None

    def is_turn_valid(self, board, column):
        is_valid = board.is_valid_location(column)
        self.game_over = not is_valid
        self.turn += 1
        return is_valid
