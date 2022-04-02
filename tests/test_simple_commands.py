import subprocess
import unittest
from pathlib import Path


class SimpleCommandsTests(unittest.TestCase):
    # Any command which reads the compstate and displays information about it
    # should be listed here. Commands which modify the compstate or which
    # require specific arguments should be tested separately.
    SIMPLE_COMMANDS = [
        'awards',
        'knocked-out-teams',
        'match-order-teams',
        'show-league-table',
        'show-schedule',
        'summary',
        'top-match-points',
        'validate',
    ]

    def test_command_snapshot(self) -> None:
        dummy_compstate = Path(__file__).parent / 'dummy'
        snapshots = Path(__file__).parent / 'snapshots'

        for command in self.SIMPLE_COMMANDS:
            with self.subTest(command):
                result = subprocess.run(
                    ['srcomp', command, str(dummy_compstate)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                self.assertEqual(0, result.returncode, result.stdout)

                snapshot = (snapshots / command).with_suffix('.txt')

                # To record a new snapshot, uncomment the following line and run the tests:
                # snapshot.write_bytes(result.stdout)

                expected = snapshot.read_bytes()
                self.assertEqual(
                    expected,
                    result.stdout,
                    "Command output unexpected content",
                )
