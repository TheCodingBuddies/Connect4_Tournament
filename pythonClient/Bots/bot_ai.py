from abc import abstractmethod, ABC


class BotAI(ABC):

    @abstractmethod
    def play(self, current_field):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def set_player_id(self, token_id):
        pass

    @abstractmethod
    def get_player_id(self):
        pass
