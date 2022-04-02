from __future__ import annotations

import argparse
from pathlib import Path
from typing import DefaultDict

from sr.comp.types import GamePoints, MatchId, TLA

__description__ = "Summaries the teams scoring the most match points"


def command(settings: argparse.Namespace) -> None:
    from collections import defaultdict
    from itertools import chain

    from sr.comp.comp import SRComp

    comp = SRComp(settings.compstate)

    all_scores = (comp.scores.tiebreaker, comp.scores.knockout, comp.scores.league)
    all_points = dict(chain.from_iterable(s.game_points.items() for s in all_scores))

    points_map: DefaultDict[GamePoints, DefaultDict[TLA, list[MatchId]]]
    points_map = defaultdict(lambda: defaultdict(list))

    for match, match_points in all_points.items():
        for tla, team_points in match_points.items():
            points_map[team_points][tla].append(match)

    count = len(points_map)

    for idx, (points, team_info) in enumerate(sorted(points_map.items())):
        if idx + 2 < count:
            print(f"{len(team_info):>3} teams scored {points}")
        else:
            print()
            print(f"The following {len(team_info)} team(s) scored {points} points:")
            for tla, matches in team_info.items():
                print(f"- {tla} in match(es): " + ", ".join(
                    "{}{}".format(*x)
                    for x in matches
                ))


def add_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        'top-match-points',
        help=__description__,
        description=__description__,
    )
    parser.add_argument(
        'compstate',
        help="competition state repo",
        type=Path,
    )
    parser.set_defaults(func=command)
