class Player:

    def __init__(self, player_id, name):
        self.name = name
        self.player_id = player_id
        self.wins = 0

    def get_name(self):
        return self.name

    def get_id(self):
        return self.player_id

    def mark_win(self):
        self.wins = self.wins + 1

    def get_wins(self):
        return self.wins
