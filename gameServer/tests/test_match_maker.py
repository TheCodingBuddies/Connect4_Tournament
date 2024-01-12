from unittest import TestCase

from gameServer.src.Tournament.match_maker import MatchMaker


class TestMatchMaker(TestCase):
    def setUp(self):
        self.match_maker = MatchMaker(4, 0)

    def test_init_match_maker(self):
        self.assertEqual(self.match_maker.match_over(), False)
