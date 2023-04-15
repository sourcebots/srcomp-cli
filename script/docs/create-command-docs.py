#!/usr/bin/env python

import subprocess
from pathlib import Path

MY_DIR = Path(__file__).parent
TEMPLATE = MY_DIR / 'template.rst'
DOCS_DIR = MY_DIR .parent.parent / 'docs' / 'commands'

import argparse

def main(args: argparse.Namespace) -> None:
    commands = subprocess.check_output(['srcomp', 'list-commands'], text=True).split()
    for command in commands:
        filename = DOCS_DIR / f"{command}.rst"
        if args.overwrite or not filename.exists():
            filename.write_text(
                TEMPLATE.read_text().format(
                    COMMAND=command,
                    UNDERLINE='=' * len(command),
                ),
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help="Replace any docs found, rather than leaving existing files unchanged",
    )
    return parser.parse_args()


if __name__  == '__main__':
    main(parse_args())
