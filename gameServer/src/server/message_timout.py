import threading
import time


class MessageTimeout:
    PLAYER_CHECK_TIMEOUT_INTERVAL_IN_S = 0.1

    def __init__(self, manual_mode, timeout_callback):
        self.timer = threading.Timer(self.PLAYER_CHECK_TIMEOUT_INTERVAL_IN_S, self.__handle_timeout)
        self.timeout_player_id = 0
        self.start_turn_timestamp = 0
        self.player_max_turn_time_in_ms = 2000 if not manual_mode else 20000000
        self.timeout_callback = timeout_callback

    def cancel(self):
        self.timer.cancel()

    def start(self):
        self.timer.start()

    def update_timeout_player(self, player_id):
        self.timeout_player_id = player_id
        self.start_turn_timestamp = time.process_time_ns()

    def active_player_has_changed(self, player_id):
        return self.timeout_player_id != player_id

    def __handle_timeout(self):
        if self.timeout_player_id != 0:
            toc = time.process_time_ns()
            elapsed_in_ms = (toc - self.start_turn_timestamp) // 1000000
            if elapsed_in_ms >= self.player_max_turn_time_in_ms:
                print("timeout for ID:", self.timeout_player_id)
                self.timeout_callback()
                return

        self.timer = threading.Timer(self.PLAYER_CHECK_TIMEOUT_INTERVAL_IN_S, self.__handle_timeout)
        self.timer.start()
