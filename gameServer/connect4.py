import sys
from time import sleep

from src.server.game_server import GameServer
from src.server.message_handler import MessageHandler
from src.tournament.match_maker import MatchMaker


def run(port, manual_mode):
    match_maker = MatchMaker(10, 0)
    message_handler = MessageHandler(manual_mode, match_maker)
    my_server = GameServer(port, message_handler)
    print("start game server..")
    my_server.start()

    while not match_maker.ready_to_play():
        pass  # wait for players

    print("start the match")
    match_maker.start_match()

    print("game finished - stop server")
    my_server.stop()

