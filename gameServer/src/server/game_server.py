import logging

from websocket_server import WebsocketServer

from src.server.message_handler import MessageHandler


class GameServer:

    def __init__(self, port, message_handler: MessageHandler):
        self.server = WebsocketServer(port=port, loglevel=logging.DEBUG)
        self.handler = message_handler
        self.server.set_fn_new_client(self.on_new_client)
        self.server.set_fn_message_received(self.on_message_received)
        self.server.set_fn_client_left(self.on_client_left)

    def start(self):
        self.server.run_forever(threaded=True)

    def stop(self):
        self.server.shutdown_gracefully()

    def sendTo(self, client, message):
        self.server.send_message(client, message)

    def on_new_client(self, client, server):
        print("connected: ", client)
        pass

    def on_client_left(self, client, server):
        print("disconnected: ", client)

    def on_message_received(self, client, server, message):
        answer = self.handler.handle(client, message)
        self.server.send_message(client, answer)
