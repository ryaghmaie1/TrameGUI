from trame.app import get_server, dev
from . import engine, ui


def _reload():
    server = get_server()
    dev.reload(ui)
    ui.initialize(server)


def main(server=None, **kwargs):
    # Get or create server
    if server is None:
        server = get_server()

    if isinstance(server, str):
        server = get_server(server)

    server.cli.add_argument("--data", help="Dataset base path", dest="data")
    args, _ = server.cli.parse_known_args()

    # Make UI reloadable (for dev)
    server.controller.on_server_reload = _reload

    # Init application
    engine.initialize(server, args.data)
    ui.initialize(server)

    # Start server
    server.start(**kwargs)


if __name__ == "__main__":
    main()
