from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


class SimpleCommandsTests(unittest.TestCase):
    # Any command which reads the compstate and displays information about it
    # should be listed here. Commands which modify the compstate should be
    # tested separately.
    SIMPLE_COMMANDS: list[tuple[str, ...]] = [
        ('awards',),
        ('knocked-out-teams',),
        ('match-order-teams',),
        ('show-league-table',),
        ('show-schedule',),
        ('summary',),
        ('top-match-points',),
        ('validate',),
    ]

    def test_command_snapshot(self) -> None:
        dummy_compstate = Path(__file__).parent / 'dummy'
        snapshots = Path(__file__).parent / 'snapshots'

        for command_parts in self.SIMPLE_COMMANDS:
            command, *args = command_parts

            with self.subTest(args):
                result = subprocess.run(
                    ['srcomp', command, str(dummy_compstate), *args],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                self.assertEqual(0, result.returncode, result.stdout.decode())

                snapshot = (snapshots / command).with_suffix('.txt')

                # To record a new snapshot, uncomment the following line and run the tests:
                # snapshot.write_bytes(result.stdout)

                expected = snapshot.read_bytes()
                self.assertEqual(
                    expected.decode(),
                    result.stdout.decode(),
                    "Command output unexpected content",
                )
