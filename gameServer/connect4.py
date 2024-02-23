from src.server.game_server import GameServer
from src.server.message_handler import MessageHandler
from src.tournament.match_maker import MatchMaker


def run(port, manual_mode):
    rounds = 10  # Anzahl Spiele
    wait_between_turns_in_ms = 0  # Wartezeit zwischen den Zügen in ms
    match_maker = MatchMaker(rounds, wait_between_turns_in_ms)
    message_handler = MessageHandler(manual_mode, match_maker)
    my_server = GameServer(port, message_handler)

    print("start game server on port", port)
    if manual_mode:
        print("manual mode is active")

    my_server.start()
    while not match_maker.ready_to_play():
        pass  # wait for players

    print("start the match")
    match_maker.start_match()

    print("game finished - stop server")
    my_server.stop()
