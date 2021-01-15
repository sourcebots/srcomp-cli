import unittest
from pathlib import Path
from unittest import mock

from sr.comp.cli.for_each_match import command


class ForEachMatchTests(unittest.TestCase):
    longMessage = True
    maxDiff = None

    def test_smoke(self):
        # Assumes that the dummy schedule is already properly formatted
        compstate_path = str(Path(__file__).parent / 'dummy')

        mock_settings = mock.Mock(
            compstate=compstate_path,
            arena=None,
            matches=set([0, 2, 3]),
            command=['spam', '{TYPE}:{ARENA}', '{NUMBER}|{TLAS}'],
        )

        with mock.patch('subprocess.check_call') as mock_check_call:
            command(mock_settings)

        mock_check_call.assert_has_calls([
            mock.call(['spam', 'league:A', '0|- CLY TTN -']),
            mock.call(['spam', 'league:B', '0|GRS QMC - -']),
            mock.call(['spam', 'league:A', '2|ICE MFG SWI BRN']),
            mock.call(['spam', 'league:B', '2|TBG EMM SGS GYG']),
            mock.call(['spam', 'league:A', '3|MAI2 HSO KDE CCR']),
            mock.call(['spam', 'league:B', '3|SCC LSS HZW MAI']),
        ])
