import random

from Bots.bot_ai import BotAI


class RandomAI(BotAI):
    def play(self, current_field):
        return random.randint(0, 6)

    def get_name(self):
        return self.name

    def set_player_id(self, token_id):
        self.token_id = token_id

    def get_player_id(self):
        return self.token_id

    def __init__(self):
        self.name = "RandomAI"
        self.token_id = None
