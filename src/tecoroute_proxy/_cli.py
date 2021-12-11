from argparse import ArgumentParser
from distutils.util import strtobool
from logging import DEBUG, INFO, basicConfig
from os import environ

from ._misc import (
    CONFIG_CONTROL,
    CONFIG_HOST,
    CONFIG_ORIGIN,
    CONFIG_PORT,
    ENTRYPOINT,
    NAME,
    SUMMARY,
    VERSION,
)
from ._server import ProxyServer


def cli() -> None:
    """Run the command-line interface."""
    envvar_pre = NAME.upper().replace("-", "_") + "_"
    parser = ArgumentParser(
        prog=ENTRYPOINT,
        description=SUMMARY,
        epilog=(
            "Most options can be provided with environment variables prefixed with "
            f'"{envvar_pre}".'
        ),
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--host",
        default=environ.get(envvar_pre + "HOST", CONFIG_HOST),
        help="The host to listen on, all interfaces if not set.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=int(environ.get(envvar_pre + "PORT", CONFIG_PORT)),
        type=int,
        help="The port to listen on.",
    )
    parser.add_argument(
        "-c",
        "--control",
        default=environ.get(envvar_pre + "CONTROL", CONFIG_CONTROL),
        help="The control path.",
    )
    parser.add_argument(
        "-o",
        "--origin",
        default=environ.get(envvar_pre + "ORIGIN", CONFIG_ORIGIN),
        help="TecoRoute service URL.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=strtobool(environ.get(envvar_pre + "VERBOSE", "n")),
        help="Verbose mode.",
    )
    parser.add_argument(
        "--version",
        action="version",
        help="Display version and exit",
        version=f"{NAME} {VERSION}",
    )
    parser.add_argument("--help", action="help", help="Display this help and exit.")
    args = parser.parse_args()
    basicConfig(level=DEBUG if args.verbose else INFO)
    proxy = ProxyServer(args.host, args.port, args.control, args.origin)
    proxy.run()
