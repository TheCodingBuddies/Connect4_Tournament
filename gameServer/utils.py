def read_start_parameter(args):
    manual_mode = "--manual-mode" in args
    server_port = 8765
    if not manual_mode and len(args) == 2:
        server_port = int(args[1])
    if manual_mode and len(args) == 3:
        server_port = int(args[2]) if args[1] == "--manual-mode" else int(args[1])

    return server_port, manual_mode
