import unittest

from sr.comp.cli.import_schedule.core import build_schedule, get_id_subsets
from sr.comp.cli.import_schedule.types import Configuration
from sr.comp.types import ArenaName, MatchNumber, TLA


class ImportScheduleTests(unittest.TestCase):
    def test_num_ids_equals_num_teams(self) -> None:
        ids = list(range(5))
        maps = list(get_id_subsets(ids, 5))

        expected = [ids]

        self.assertEqual(
            expected,
            maps,
            "Only one possible combination when same number of ids as teams",
        )

    def test_one_spare_id(self) -> None:
        ids = list(range(3))
        num_teams = 2

        ids_set = set(ids)

        subsets = list(get_id_subsets(ids, num_teams))

        self.assertEqual(
            3,
            len(subsets),
            "Should have as many maps as valid permutations",
        )

        # Don't actually care what the mappings are, only that all are explored
        ids_omitted = []
        for subset in subsets:
            ids_used = set(subset)
            omitted = ids_set - ids_used

            self.assertEqual(1, len(omitted), "Omitted wrong number of ids")
            ids_omitted.append(omitted.pop())

        self.assertEqual(
            set(ids_omitted),
            ids_set,
            "Should have omitted each id once",
        )

    def test_two_spare_ids(self) -> None:
        ids = list(range(4))
        num_teams = 2

        ids_set = set(ids)

        subsets = list(get_id_subsets(ids, num_teams))

        expected_omitted = set(["0,1", "0,2", "0,3", "1,2", "1,3", "2,3"])

        self.assertEqual(
            len(expected_omitted),
            len(subsets),
            "Should have as many maps as valid permutations",
        )

        # Don't actually care what the mappings are, only that all are explored
        ids_omitted = []
        for subset in subsets:
            ids_used = set(subset)
            omitted = ids_set - ids_used

            self.assertEqual(2, len(omitted), "Omitted wrong number of ids")
            ids_omitted.append(",".join(map(str, sorted(omitted))))

        self.assertEqual(
            expected_omitted,
            set(ids_omitted),
            "Should have omitted each id pair once",
        )

    def test_build_schedule(self) -> None:
        lines = ['0|1|2|3', '1|2|3|4']
        teams = [TLA('ABC'), TLA('DEF'), TLA('GHI')]

        matches, bad = build_schedule(
            Configuration(
                [ArenaName('A')],
                teams,
                teams_per_game=4,
                first_match_number=MatchNumber(0),
            ),
            lines,
            ids_to_ignore=[],
        )

        expected_matches = {
            0: {'A': [None, 'ABC', 'DEF', 'GHI']},
            1: {'A': ['ABC', 'DEF', 'GHI', None]},
        }

        self.assertEqual(expected_matches, matches, "Wrong matches")

        self.assertEqual([], bad, "Should not be any 'bad' matches")

    def test_extend_schedule(self) -> None:
        lines = ['0|1|2|3', '1|2|3|4']
        teams = [TLA('ABC'), TLA('DEF'), TLA('GHI')]

        matches, bad = build_schedule(
            Configuration(
                [ArenaName('A')],
                teams,
                teams_per_game=4,
                first_match_number=MatchNumber(4),
            ),
            lines,
            ids_to_ignore=[],
        )

        expected_matches = {
            4: {'A': [None, 'ABC', 'DEF', 'GHI']},
            5: {'A': ['ABC', 'DEF', 'GHI', None]},
        }

        self.assertEqual(expected_matches, matches, "Wrong matches")

        self.assertEqual([], bad, "Should not be any 'bad' matches")

    def test_build_schedule_appearance_order(self) -> None:
        lines = ['3|1|0|4', '1|2|4|0']
        teams = [TLA('ABC'), TLA('DEF'), TLA('GHI')]

        matches, bad = build_schedule(
            Configuration(
                [ArenaName('A')],
                teams,
                teams_per_game=4,
                first_match_number=MatchNumber(0),
            ),
            lines,
            ids_to_ignore=[],
        )

        expected_matches = {
            0: {'A': [None, 'ABC', 'DEF', 'GHI']},
            1: {'A': ['ABC', None, 'GHI', 'DEF']},
        }

        self.assertEqual(expected_matches, matches, "Wrong matches")

        self.assertEqual([], bad, "Should not be any 'bad' matches")
