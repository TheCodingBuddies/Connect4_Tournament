from unittest import TestCase

from utils import read_start_parameter


class Test(TestCase):
    def test_use_standard_port_without_manual_mode_by_default(self):
        (port, manual_mode) = read_start_parameter(["main.py"])
        self.assertEqual(8765, port)
        self.assertEqual(False, manual_mode)

    def test_use_specific_port_without_manual_mode(self):
        (port, manual_mode) = read_start_parameter(["main.py", "5656"])
        self.assertEqual(5656, port)
        self.assertEqual(False, manual_mode)

    def test_activate_manual_mode_without_changing_default_port(self):
        (port, manual_mode) = read_start_parameter(["main.py", "--manual-mode"])
        self.assertEqual(8765, port)
        self.assertEqual(True, manual_mode)

    def test_define_both_parameter_port_first(self):
        (port, manual_mode) = read_start_parameter(["main.py", "5555", "--manual-mode"])
        self.assertEqual(5555, port)
        self.assertEqual(True, manual_mode)

    def test_define_both_parameter_port_last(self):
        (port, manual_mode) = read_start_parameter(["main.py", "--manual-mode", "6666"])
        self.assertEqual(6666, port)
        self.assertEqual(True, manual_mode)
