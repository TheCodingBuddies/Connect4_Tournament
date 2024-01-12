class GameStatistics:

    def __init__(self):
        self.player_wins = []
        self.games_played = 0

    def update_statistics(self, winner):
        self.games_played += 1
        found_player = self.__find(winner)
        if found_player:
            found_player["wins"] = found_player["wins"] + 1
        else:
            self.player_wins.append({"id": winner.get_id(), "player": winner, "wins": 1})

    def get_win_ratio(self, player):
        found_player = self.__find(player)
        if self.games_played <= 0:
            return 0
        return (found_player["wins"] / self.games_played) * 100 if found_player else 0

    def get_total_wins(self, player):
        found_player = self.__find(player)
        return found_player["wins"] if found_player else 0

    def get_winner(self):
        highest_entry = max(self.player_wins, key=lambda player: player["wins"])
        count_highest_wins = sum(1 for player in self.player_wins if player["wins"] == highest_entry["wins"])
        if count_highest_wins == 1:
            return highest_entry["player"]
        else:
            return None

    def __find(self, player):
        return next((p for p in self.player_wins if p["id"] == player.get_id()), None)
