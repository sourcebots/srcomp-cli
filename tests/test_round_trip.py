import unittest
from pathlib import Path
from typing import Tuple
from unittest import mock

from sr.comp.cli.yaml_round_trip import command


class RoundTripTests(unittest.TestCase):
    maxDiff = 8000

    def get_info(self, file_path: Path) -> Tuple[float, str]:
        return file_path.stat().st_mtime, file_path.read_text()

    def test_dummy_schedule(self) -> None:
        # Assumes that the dummy schedule is already properly formatted
        dummy_schedule = Path(__file__).parent / 'dummy' / 'schedule.yaml'

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
