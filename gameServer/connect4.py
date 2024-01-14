import asyncio
import os
import threading

from src.server.server import Server
from src.tournament.match_maker import MatchMaker


def run(port):
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    my_server = Server('localhost', port, MatchMaker(10, 0))

    thread = threading.Thread(target=my_server.start_server, args=(loop, future))
    thread.start()

    while my_server.get_player_count() < 2:
        my_server.get_player_count()

    print("start the match")
    my_server.start_match()
    print("Stopping event loop")
    my_server.stop_server(loop, future)
    print("Waiting for termination")
    thread.join(1)
    if thread.is_alive():
        os._exit(0)
