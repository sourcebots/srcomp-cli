import collections
from pathlib import Path
from typing import List

from sr.comp.types import TLA


def order_teams(compstate_path: Path, team_ids: List[TLA]) -> List[TLA]:
    """
    Order teams either randomly or, if there's a layout available, by location.
    """
    import yaml

    from sr.comp.knockout_scheduler.stable_random import Random
    from sr.comp.validation import join_and

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

    if len(layout_teams) != len(ordered_teams):
        duplicates = [x for x, y in collections.Counter(ordered_teams).items() if y > 1]
        raise ValueError(f"Some teams appear twice in the layout! {join_and(duplicates)}")

    all_teams = set(team_ids)
    missing = all_teams - layout_teams
    if missing:
        raise ValueError(f"Some teams not in layout: {join_and(missing)}.")

    extra = layout_teams - all_teams
    if extra:
        print(f"WARNING: Extra teams in layout will be ignoreed: {join_and(extra)}.")
        for tla in extra:
            ordered_teams.remove(tla)

    return ordered_teams
