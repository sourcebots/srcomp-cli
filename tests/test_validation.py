import subprocess
import unittest
from pathlib import Path


class ValidationTests(unittest.TestCase):
    def test_dummy_is_valid(self) -> None:
        dummy_compstate = Path(__file__).parent / 'dummy'

        result = subprocess.run(
            ['srcomp', 'validate', str(dummy_compstate)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self.assertEqual(0, result.returncode, result.stdout)
