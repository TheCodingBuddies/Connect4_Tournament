import sys
from connect4 import run
from utils import read_start_parameter

if __name__ == '__main__':
    (port, manual_mode) = read_start_parameter(sys.argv)

    run(port, manual_mode)
