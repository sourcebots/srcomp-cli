import collections
from typing import Dict, Iterator, List, Mapping, Optional, Tuple, TypeVar

from sr.comp.types import ArenaName, MatchNumber, TLA

from . import loading
from .types import BadMatch, ID, RawMatch

T = TypeVar('T')


def chunks_of_size(list_: List[T], size: int) -> Iterator[List[T]]:
    if len(list_) % size != 0:
        raise ValueError(
            "Unable to chunk list whose size is not evenly divisble by given "
            f"size {size}.",
        )

    list_ = list_[:]
    while len(list_):
        chunk = []
        for _ in range(size):
            chunk.append(list_.pop(0))
        yield chunk


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
    matches = {}
    bad_matches = []
    for match_num, match_ids in enumerate(schedule):
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
    ids, schedule = loading.load_ids_schedule(
        schedule_lines,
        num_arenas=len(arena_ids),
        teams_per_game=teams_per_game,
    )

    # Ignore any ids we've been told to
    if ids_to_ignore:
        ignore_ids(ids, ids_to_ignore)

    # Sanity checks
    if len(ids) < len(team_ids):
        raise ValueError(
            f"Not enough places in the schedule (need {len(ids)}, got {len(team_ids)}).",
        )

    # Get matches
    matches, bad_matches = get_best_fit(
        ids,
        team_ids,
        schedule,
        arena_ids,
        teams_per_game,
    )

    return matches, bad_matches
