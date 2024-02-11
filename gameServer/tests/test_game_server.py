from unittest import TestCase
from unittest.mock import Mock, patch

from src.server.game_server import GameServer


class TestServer(TestCase):

    def setUp(self):
        self.mocked_message_handler = Mock()
        self.server = GameServer(8765, self.mocked_message_handler)

    @patch('websocket_server.WebsocketServer.run_forever')
    def test_run_server_forever_on_start(self, run_forever):
        self.server.start()
        run_forever.assert_called_once_with(threaded=True)

    @patch('websocket_server.WebsocketServer.shutdown_gracefully')
    def test_run_server_forever_on_start(self, shutdown_gracefully):
        self.server.stop()
        shutdown_gracefully.assert_called_once()

    @patch('websocket_server.WebsocketServer.send_message')
    def test_response_answer_of_message_handler(self, send_message):
        self.mocked_message_handler.handle.return_value = "response"
        self.server.server.clients = [{"id": 1}]

        self.server.on_message_received({"id": 1}, {}, "received_message")
        self.mocked_message_handler.handle.assert_called_once()
        send_message.assert_called_once_with({"id": 1}, "response")
