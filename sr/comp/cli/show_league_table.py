"""Show the current state of the league table"""

from __future__ import annotations

import argparse
from typing import Any, Callable, NamedTuple

from league_ranker import LeaguePoints

from sr.comp.scores import LeaguePosition
from sr.comp.types import GamePoints, TLA


class Row(NamedTuple):
    position: LeaguePosition
    league_points: LeaguePoints
    game_points: GamePoints
    tla: TLA
    name: str


class SortSpec(NamedTuple):
    key: Callable[[Row], Any]
    reverse: bool


SORT_TYPES = {
    'rank': SortSpec(lambda x: x.position, False),
    'game': SortSpec(lambda x: x.game_points, True),
    'team': SortSpec(lambda x: x.name, False),
}


def command(args: argparse.Namespace) -> None:
    import os.path
    from collections import Counter

    from tabulate import tabulate

    from sr.comp.comp import SRComp

    comp = SRComp(os.path.realpath(args.compstate))

    tie_count = Counter(comp.scores.league.positions.values())
    tied_positions = set(x for x, y in tie_count.items() if y > 1)

    league_table = []
    for team in comp.teams.values():
        scores = comp.scores.league.teams[team.tla]
        league_pos = comp.scores.league.positions[team.tla]
        league_table.append(Row(
            league_pos,
            scores.league_points,
            scores.game_points,
            team.tla,
            team.name,
        ))

    key, reverse = SORT_TYPES[args.sort]
    league_table.sort(key=key, reverse=reverse)

    print(tabulate(
        [
            [
                f"={x.position}" if x.position in tied_positions else x.position,
                x.league_points,
                x.game_points,
                f"{x.tla}: {x.name}",
            ]
            for x in league_table
        ],
        headers=["Rank", "League", "Game", "Team"],
        tablefmt='github',
        colalign=('center', 'center', 'center', 'left'),  # left-align team names
    ))


def add_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        'show-league-table',
        help=__doc__,
        description=__doc__,
    )
    parser.add_argument(
        'compstate',
        help="competition state repo",
    )
    parser.add_argument(
        '--sort',
        choices=SORT_TYPES.keys(),
        default='rank',
        help="Sort table by a column",
    )
    parser.set_defaults(func=command)
