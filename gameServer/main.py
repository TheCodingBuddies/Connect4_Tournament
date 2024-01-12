import asyncio
import os
import sys
import threading

sys.path.append("src")
sys.path.append("src/Game")
sys.path.append("src/Renderer")
sys.path.append("src/Server")
sys.path.append("src/Statistics")
sys.path.append("src/Tournament")

from src.Server.server import Server
from src.Tournament.match_maker import MatchMaker


if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) == 2 else 8765
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    my_server = Server('localhost', port, MatchMaker(10, 0))

    thread = threading.Thread(target=my_server.start_server, args=(loop, future))
    thread.start()

    while my_server.get_player_count() < 2:
        my_server.get_player_count()

    print("now start the match")
    my_server.start_match()
    print("Stopping event loop")
    my_server.stop_server(loop, future)
    print("Waiting for termination")
    thread.join(1)
    if thread.is_alive():
        os._exit(0)
