from Bots.bot_ai import BotAI


class FillAI(BotAI):
    next_column = 0

    def play(self, current_field):
        return self.next_column

    def get_name(self):
        return self.name

    def set_player_id(self, token_id):
        self.token_id = token_id

    def get_player_id(self):
        return self.token_id

    def __init__(self):
        self.name = "FillAI"
        self.token_id = None
