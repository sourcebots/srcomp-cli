import os.path
import subprocess
import unittest


class ValidationTests(unittest.TestCase):
    def test_dummy_is_valid(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        dummy_compstate = os.path.join(test_dir, 'dummy')

        result = subprocess.run(
            ['srcomp', 'validate', dummy_compstate],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self.assertEqual(0, result.returncode, result.stdout)
