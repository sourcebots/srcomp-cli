"""
Import a league.yaml from a schedule file.

A schedule file specifies matches one-per-line, as follows:

A 'match' consists of a number of unique identifiers separated by pipe
characters. The total number of identifiers in the file should be equal
to or greater than the number of teams in the compstate.

The number of identifiers in a given match must be a multiple of the
number of teams per game (currently 4), up to the number of arenas in
the compstate.

Whitespace (other than newlines) within the file is ignored, as is any
content to the right of a hash character (#), including the hash. As a
result hash characters may be used to start line comments.

Example schedules for 48, 52 or 56 teams are available  at:
https://github.com/PeterJCLaw/srobo-schedules/tree/master/seed_schedules
"""

import argparse
import collections
from pathlib import Path
from typing import (
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    NamedTuple,
    NewType,
    Optional,
    Tuple,
    TypeVar,
)

from sr.comp.types import ArenaName, MatchNumber, TLA

T = TypeVar('T')
ID = NewType('ID', str)
RawMatch = Dict[ArenaName, List[Optional[TLA]]]


class BadMatch(NamedTuple):
    arena: ArenaName
    num: MatchNumber
    num_teams: int


def parse_ids(ids: str, sep: str = ',') -> List[ID]:
    return [ID(x) for x in ids.split(sep)]


def tidy(lines: Iterable[str]) -> List[str]:
    "Strip comments and trailing whitespace"
    schedule = []
    for line in lines:
        idx = line.find('#')
        if idx > -1:
            line = line[:idx]

        line = line.strip()

        if line:
            schedule.append(line)

    return schedule


def chunks_of_size(list_: List[T], size: int) -> Iterator[List[T]]:
    list_ = list_[:]
    assert len(list_) % size == 0
    while len(list_):
        chunk = []
        for _ in range(size):
            chunk.append(list_.pop(0))
        yield chunk


def league_yaml_path(compstate_path: Path) -> Path:
    return compstate_path / 'league.yaml'


def dump_league_yaml(
    matches: Dict[MatchNumber, RawMatch],
    file_path: Path,
) -> None:
    import yaml

    with open(file_path, 'w') as lfp:
        empty = {'matches': matches}
        yaml.dump(empty, lfp)


def load_teams_areans(compstate_path: Path) -> Tuple[List[TLA], List[ArenaName], int]:
    from sr.comp import arenas, teams

    team_ids = sorted(teams.load_teams(compstate_path / 'teams.yaml').keys())
    arenas_yaml = compstate_path / 'arenas.yaml'
    arena_ids = sorted(arenas.load_arenas(arenas_yaml).keys())
    num_corners = len(arenas.load_corners(arenas_yaml))

    return team_ids, arena_ids, num_corners


def load_ids_schedule(schedule_lines: Iterable[str]) -> Tuple[List[ID], List[List[ID]]]:
    """
    Converts an iterable of strings containing pipe-separated ids into
    a tuple: ``(ids, schedule)``. The ``ids`` is a list of unique ids
    in the order which they first appear, the ``schedule`` is a list of
    lists of ids in each line.
    """

    ids: List[ID] = []
    schedule: List[List[ID]] = []
    for match in schedule_lines:
        match_ids = parse_ids(match, sep='|')
        uniq_match_ids = set(match_ids)
        assert len(match_ids) == len(uniq_match_ids), match_ids
        schedule.append(match_ids)

        for id_ in match_ids:
            if id_ not in ids:
                ids.append(id_)

    return ids, schedule


def ignore_ids(ids: List[ID], ids_to_remove: List[ID]) -> None:
    for i in ids_to_remove:
        ids.remove(i)


def get_id_subsets(ids: List[T], limit: int) -> Iterator[List[T]]:
    num_ids = len(ids)

    extra = num_ids - limit

    if extra == 0:
        # Only one posibility -- use all of them
        yield ids

    elif extra == 1:
        for idx in range(len(ids)):
            ids_clone = ids[:]
            ids_clone.pop(idx)
            yield ids_clone

    elif extra == 2:
        for idx1 in range(len(ids)):
            for idx2 in range(idx1 + 1, len(ids)):
                ids_clone = ids[:]
                ids_clone.pop(idx2)
                ids_clone.pop(idx1)
                yield ids_clone

    elif extra == 3:
        for idx1 in range(len(ids)):
            for idx2 in range(idx1 + 1, len(ids)):
                for idx3 in range(idx2 + 1, len(ids)):
                    ids_clone = ids[:]
                    ids_clone.pop(idx3)
                    ids_clone.pop(idx2)
                    ids_clone.pop(idx1)
                    yield ids_clone

    else:
        # TODO: consider generalising the above or adding more handling
        raise Exception("Too many empty slots to compensate for ({0}).".format(extra))


def build_id_team_maps(ids: List[ID], team_ids: List[TLA]) -> Iterator[Dict[ID, TLA]]:
    # If there are more ids than team_ids we want to ensure that we minimize
    # the number of matches which have empty places and also the number of
    # empty places in any given match.
    # This function generates possible mappings of ids to teams as needed
    # in order to explore excluding different ids.
    #
    # Note: this function does _not_ explore mapping the same subset of
    # ids to the given teams since that doesn't achieve any changes in
    # which matches have empty spaces.

    for id_subset in get_id_subsets(ids, len(team_ids)):
        yield dict(zip(id_subset, team_ids))


def build_matches(
    id_team_map: Dict[ID, TLA],
    schedule: List[List[ID]],
    arena_ids: List[ArenaName],
    teams_per_game: int,
) -> Tuple[
    Dict[MatchNumber, RawMatch],
    List[BadMatch],
]:
    num_arenas = len(arena_ids)

    matches = {}
    bad_matches = []
    for match_num, match_ids in enumerate(schedule):
        assert len(match_ids) / teams_per_game <= num_arenas, \
            "Match {0} has too many ids".format(match_num)
        assert len(match_ids) % teams_per_game == 0, \
            "Match {0} has incompatible number of ids".format(match_num)

        match_teams = [id_team_map.get(id_) for id_ in match_ids]
        games = chunks_of_size(match_teams, teams_per_game)

        matches[MatchNumber(match_num)] = match = dict(zip(arena_ids, games))

        # Check that the match has enough actual teams; warn if not
        for arena, teams in match.items():
            num_teams = len(set(teams) - set([None]))
            if num_teams <= (teams_per_game / 2):
                bad_matches.append(BadMatch(arena, MatchNumber(match_num), num_teams))

    return matches, bad_matches


def are_better_matches(
    best: List[BadMatch],
    new: List[BadMatch],
    teams_per_game: int,
) -> bool:
    def get_empty_places_map(bad_matches: List[BadMatch]) -> Mapping[int, int]:
        empty_places_map: Dict[int, int] = collections.Counter()
        for bad_match in bad_matches:
            num_empty = teams_per_game - bad_match.num_teams
            empty_places_map[num_empty] += 1
        return empty_places_map

    best_map = get_empty_places_map(best)
    new_map = get_empty_places_map(new)

    possible_empty_places = set(list(best_map.keys()) + list(new_map.keys()))

    # Even single matches with lots of empty slots are bad
    for num_empty_places in sorted(possible_empty_places, reverse=True):
        if new_map[num_empty_places] < best_map[num_empty_places]:
            return True

    return False


def get_best_fit(
    ids: List[ID],
    team_ids: List[TLA],
    schedule: List[List[ID]],
    arena_ids: List[ArenaName],
    teams_per_game: int,
) -> Tuple[
    Dict[MatchNumber, RawMatch],
    List[BadMatch],
]:
    best: Optional[Tuple[
        Dict[MatchNumber, RawMatch],
        List[BadMatch],
    ]] = None
    for id_team_map in build_id_team_maps(ids, team_ids):
        matches, bad_matches = build_matches(
            id_team_map,
            schedule,
            arena_ids,
            teams_per_game,
        )

        if len(bad_matches) == 0:
            # Nothing bad about these, ship them
            return matches, bad_matches

        if best is None or are_better_matches(best[1], bad_matches, teams_per_game):
            best = (matches, bad_matches)

    assert best is not None

    return best


def order_teams(compstate_path: Path, team_ids: List[TLA]) -> List[TLA]:
    """
    Order teams either randomly or, if there's a layout available, by location.
    """
    import yaml

    from sr.comp.knockout_scheduler.stable_random import Random

    layout_yaml = compstate_path / 'layout.yaml'
    if not layout_yaml.exists():
        # No layout; go random
        random = Random()
        random.seed("".join(team_ids).encode())
        random.shuffle(team_ids)
        return team_ids

    with open(layout_yaml, 'r') as lf:
        layout_raw = yaml.load(lf)
        layout = layout_raw['teams']

    ordered_teams = []
    for group in layout:
        ordered_teams += group['teams']

    layout_teams = set(ordered_teams)
    assert len(layout_teams) == len(ordered_teams), "Some teams appear twice in the layout!"

    all_teams = set(team_ids)
    missing = all_teams - layout_teams
    assert not missing, "Some teams not in layout: {0}.".format(", ".join(missing))

    all_teams = set(team_ids)
    extra = layout_teams - all_teams
    if extra:
        print("WARNING: Extra teams in layout will be ignoreed: {0}.".format(
            ", ".join(extra),
        ))
        for tla in extra:
            ordered_teams.remove(tla)

    return ordered_teams


def build_schedule(
    schedule_lines: List[str],
    ids_to_ignore: List[ID],
    team_ids: List[TLA],
    arena_ids: List[ArenaName],
    teams_per_game: int,
) -> Tuple[
    Dict[MatchNumber, RawMatch],
    List[BadMatch],
]:
    # Collect up the ids used
    ids, schedule = load_ids_schedule(schedule_lines)

    # Ignore any ids we've been told to
    if ids_to_ignore:
        ignore_ids(ids, ids_to_ignore)

    # Sanity checks
    num_ids = len(ids)
    num_teams = len(team_ids)
    assert num_ids >= num_teams, "Not enough places in the schedule " \
                                 "(need {0}, got {1}).".format(num_ids, num_teams)

    # Get matches
    matches, bad_matches = get_best_fit(
        ids,
        team_ids,
        schedule,
        arena_ids,
        teams_per_game,
    )

    return matches, bad_matches


def command(args: argparse.Namespace) -> None:
    with open(args.schedule, 'r') as sfp:
        schedule_lines = tidy(sfp.readlines())

    # Grab the teams and arenas
    try:
        team_ids, arena_ids, teams_per_game = load_teams_areans(args.compstate)
    except Exception as e:
        print("Failed to load existing state ({0}).".format(e))
        print("Make it valid (consider removing the league.yaml and layout.yaml)")
        print("and try again.")
        exit(1)

    # Semi-randomise
    team_ids = order_teams(args.compstate, team_ids)

    matches, bad_matches = build_schedule(
        schedule_lines,
        args.ignore_ids,
        team_ids,
        arena_ids,
        teams_per_game,
    )

    # Print any warnings about the matches
    for bad_match in bad_matches:
        tpl = "Warning: match {arena}:{num} only has {num_teams} teams."
        print(tpl.format(**bad_match._asdict()))

    # Save the matches to the file
    league_yaml = league_yaml_path(args.compstate)
    dump_league_yaml(matches, league_yaml)


def add_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        'import-schedule',
        help="Import a league.yaml file from a schedule file",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '-i',
        '--ignore-ids',
        type=parse_ids,
        help="comma separated list of ids to ignore",
    )
    parser.add_argument('compstate', type=Path, help="competition state repository")
    parser.add_argument('schedule', type=Path, help="schedule to import")
    parser.set_defaults(func=command)
