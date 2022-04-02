import os.path
import subprocess
import unittest


class LeagueTableTests(unittest.TestCase):
    def test_league_table_succeeds(self) -> None:
        test_dir = os.path.dirname(os.path.abspath(__file__))
        dummy_compstate = os.path.join(test_dir, 'dummy')

        result = subprocess.run(
            ['srcomp', 'show-league-table', dummy_compstate],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self.assertEqual(0, result.returncode, result.stdout)
