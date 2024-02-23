import sys
from connect4 import run

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) >= 2 else 8765
    manual_mode = True if "--manual-mode" in sys.argv else False
    run(port, manual_mode)
