from Game.player import Player


class GameConfig:

    def __init__(self, rows, columns, speed_ms, player1: Player, player2: Player):
        self.rows = rows
        self.columns = columns
        self.player_one = player1
        self.player_two = player2
        self.speed_ms = speed_ms

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns

    def get_player_one(self):
        return self.player_one

    def get_player_two(self):
        return self.player_two

    def get_speed(self):
        return self.speed_ms
