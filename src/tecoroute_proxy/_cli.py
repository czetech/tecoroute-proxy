from argparse import ArgumentParser, Namespace
from asyncio import Event, get_event_loop, run, set_event_loop_policy
from logging import DEBUG, INFO, basicConfig
from signal import SIGINT, SIGTERM

from ._misc import CONTROL, HOST, ORIGIN, PORT, dist
from ._server import ProxyServer

try:
    from uvloop import EventLoopPolicy
except ImportError:
    pass
else:
    set_event_loop_policy(EventLoopPolicy())


async def _main(args: Namespace) -> None:
    basicConfig(level=DEBUG if args.verbose else INFO)
    proxy_server = ProxyServer(args.host, args.port, args.control, args.origin)
    await proxy_server.start()
    runner = Event()
    for signum in (SIGINT, SIGTERM):
        get_event_loop().add_signal_handler(signum, lambda: runner.set())
    await runner.wait()
    await proxy_server.stop()


def cli() -> None:
    """Run the command-line interface."""
    parser = ArgumentParser(
        prog=dist.entry_points[0].name, description=dist.metadata["Summary"]
    )
    parser.add_argument(
        "-H",
        "--host",
        default=HOST,
        help="host to listen on, all interfaces if not set",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=PORT,
        type=int,
        help="port to listen on",
    )
    parser.add_argument(
        "-c",
        "--control",
        default=CONTROL,
        help="control path",
    )
    parser.add_argument(
        "-o",
        "--origin",
        default=ORIGIN,
        help="TecoRoute service URL",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="verbose mode",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"TecoRoute Proxy {dist.version}",
    )
    run(_main(parser.parse_args()))
