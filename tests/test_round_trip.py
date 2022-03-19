import os
import unittest
from unittest import mock

from sr.comp.cli.yaml_round_trip import command


class RoundTripTests(unittest.TestCase):
    maxDiff = 8000

    def get_info(self, file_path):
        mod = os.stat(file_path).st_mtime

        with open(file_path, 'r') as f:
            content = f.read()

        return mod, content

    def test_dummy_schedule(self):
        # Assumes that the dummy schedule is already properly formatted
        test_dir = os.path.dirname(os.path.abspath(__file__))
        dummy_schedule = os.path.join(test_dir, 'dummy', 'schedule.yaml')

        orig_mod, orig_content = self.get_info(dummy_schedule)

        mock_settings = mock.Mock(file_path=dummy_schedule)
        command(mock_settings)

        new_mod, new_content = self.get_info(dummy_schedule)

        self.assertNotEqual(orig_mod, new_mod, "Should have rewritten the file")
        self.assertEqual(
            orig_content,
            new_content,
            "Should not have changed file content",
        )
