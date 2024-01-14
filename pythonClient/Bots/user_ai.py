from Bots.bot_ai import BotAI


class UserAI(BotAI):
    def play(self, current_field):
        #
        # Implementiere hier deine Logik, damit die KI spielen kann
        #
        return 0  # aktuell wird immer die erste Spalte ausgewählt als nächsten Zug

    def get_name(self):
        return self.name

    def set_player_id(self, token_id):
        self.token_id = token_id

    def get_player_id(self):
        return self.token_id

    def __init__(self):
        # Wähle hier deinen Nickname aus (ändere "UserAI")
        self.name = "UserAI"
        self.token_id = None  # Die Token ID wird vom Server vergeben.. nicht editieren!
