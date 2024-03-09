"""
Fetch the deployed revisions of the compstate from all known hosts.

This will fetch revisions of the compstate from its 'origin' git remote and from
its various deployments.
"""

from __future__ import annotations

import argparse
import sys


def command(args: argparse.Namespace) -> None:
    from sr.comp.cli.deploy import (
        BOLD,
        ENDC,
        FAIL,
        get_current_state,
        get_deployments,
        ref_compstate,
    )
    from sr.comp.raw_compstate import RawCompstate

    compstate = RawCompstate(args.compstate, local_only=False)
    hosts = get_deployments(compstate)

    print("Fetching upstream... ", end="")
    sys.stdout.flush()
    compstate.fetch()
    print("done.")

    for host in hosts:
        print(f"Fetching {host}... {BOLD}{FAIL}", end="")
        sys.stdout.flush()

        # In case of error `get_current_state` prints the error and returns `None`.
        state = get_current_state(host)
        if not state:
            continue

        compstate.fetch(ref_compstate(host), [state], quiet=True)
        print(f"{ENDC}{state} fetched.")


def add_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    help_msg, *_ = __doc__.strip().splitlines()
    parser = subparsers.add_parser(
        'fetch',
        help=help_msg,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('compstate', help="competition state repository")
    parser.set_defaults(func=command)
