"""
Run the SRComp Scorer UI. Requires ``sr.comp.scorer`` to be installed.
"""

from __future__ import annotations

import argparse
from typing import cast


def find_unused_port() -> int:
    import socket

    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.bind(('::1', 0))
    print(sock.getsockname())
    addr, port, flowinfo, scopeid = sock.getsockname()
    sock.close()
    # getsockname's return type is not specified as it differs by socket family.
    # For IPv6 it's an integer.
    return cast(int, port)


def command(settings: argparse.Namespace) -> None:
    import threading
    import time
    import webbrowser

    try:
        import sr.comp.scorer  # type: ignore[import]
    except ImportError:
        print("sr.comp.scorer not installed.")
        exit(1)

    port = find_unused_port()
    app = sr.comp.scorer.app
    app.config['COMPSTATE'] = settings.compstate
    app.config['COMPSTATE_LOCAL'] = not settings.push_changes

    def browse() -> None:
        time.sleep(1.5)
        webbrowser.open(f'http://localhost:{port}/')

    thread = threading.Thread(target=browse)
    thread.start()

    try:
        app.run(
            host='::1',
            port=port,
            debug=False,
            passthrough_errors=True,
        )
    except KeyboardInterrupt:
        pass


def add_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        'score',
        help=__doc__.strip().splitlines()[0],
        description=__doc__,
    )
    parser.add_argument('compstate', help="competition state repository")
    parser.add_argument(
        '-p',
        '--push-changes',
        action='store_true',
        help="send commits upstream to origin/master",
    )
    parser.set_defaults(func=command)
