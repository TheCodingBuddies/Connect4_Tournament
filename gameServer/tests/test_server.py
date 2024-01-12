from unittest import TestCase
from unittest.mock import Mock

from gameServer.src.Server.server import Server


class TestServer(TestCase):

    def setUp(self):
        match_maker = Mock()
        self.server = Server("127.0.0.1", 80, match_maker)
