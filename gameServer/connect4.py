from src.server.game_server import GameServer
from src.server.message_handler import MessageHandler


def run(port, manual_mode):
    message_handler = MessageHandler(manual_mode)
    my_server = GameServer(port, message_handler)
    my_server.start()

    while message_handler.get_player_count() < 2:
        message_handler.get_player_count()

    print("start the match")
    message_handler.start_match()

    my_server.stop()

