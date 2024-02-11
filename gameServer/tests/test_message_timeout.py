import time
from unittest import TestCase
from unittest.mock import patch, Mock

from src.server.message_timout import MessageTimeout


class TestMessageTimeout(TestCase):

    def setUp(self):
        pass
        self.timeout = MessageTimeout(True, Mock())

    def test_no_timeouts_on_manual_mode(self):
        self.timeout = MessageTimeout(True, Mock())
        self.assertEqual(self.timeout.player_max_turn_time_in_ms, 20000000)

    def test_2_seconds_timeouts_on_AI_mode(self):
        self.timeout = MessageTimeout(False, Mock())
        self.assertEqual(self.timeout.player_max_turn_time_in_ms, 2000)

    @patch('time.process_time_ns')
    def test_update_timeout_player(self, mocked_process_time_ns):
        mocked_process_time_ns.return_value = 100
        self.timeout.update_timeout_player(1)

        self.assertEqual(self.timeout.timeout_player_id, 1)
        self.assertEqual(self.timeout.start_turn_timestamp, 100)

    def test_timeout_player_has_changed(self):
        self.timeout.timeout_player_id = 2
        self.assertTrue(self.timeout.active_player_has_changed(1))

    def test_timeout_player_has_not_changed(self):
        self.timeout.timeout_player_id = 1
        self.assertFalse(self.timeout.active_player_has_changed(1))

    @patch('time.process_time_ns')
    def test_callback_called_after_100ms(self, mocked_process_time_ns):
        mocked_process_time_ns.return_value = 1000000000000000000000
        mocked_callback = Mock()
        self.timeout = MessageTimeout(True, mocked_callback)
        self.timeout.timeout_player_id = 1
        self.timeout.start()
        time.sleep(0.20)
        self.timeout.cancel()
        mocked_callback.assert_called_once()
