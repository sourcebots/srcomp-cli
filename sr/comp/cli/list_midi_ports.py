from __future__ import annotations

import argparse

__description__ = "List available MIDI output ports."


def command(args: argparse.Namespace) -> None:
    import mido  # type: ignore[import]

    ports = mido.get_output_names()
    print(len(ports), "outputs:")
    for port in ports:
        print("-", port)


def add_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        'list-midi-ports',
        help=__description__,
        description=__description__,
    )
    parser.set_defaults(func=command)
