from __future__ import annotations

import argparse


def command(settings: argparse.Namespace) -> None:
    from sr.comp.comp import SRComp
    from sr.comp.validation import validate

    comp = SRComp(settings.compstate)

    if settings.lax:
        error_count = 0
    else:
        error_count = validate(comp)

    exit(error_count)


def add_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    help_msg = "Check that the compstate can be loaded and represents a valid state."
    parser = subparsers.add_parser(
        'validate',
        help=help_msg,
        description=help_msg,
    )
    parser.add_argument('compstate', help="competition state repository")
    parser.add_argument(
        '-l',
        '--lax',
        action='store_true',
        help="only check if it loads, rather than run a validation",
    )
    parser.set_defaults(func=command)
