__description__ = "Show the current state of the league table"


SORT_TYPES = {  # cli string: (sort column, sort direction)
    'position': (0, False),
    'game': (2, True),
    'team': (3, False),
}

def command(settings):
    import os.path
    from collections import defaultdict
    from functools import partial
    from itertools import chain

    from sr.comp.comp import SRComp

    comp = SRComp(os.path.realpath(settings.compstate))

    league_table = []
    for team in comp.teams.values():
        scores = comp.scores.league.teams[team.tla]
        league_pos = comp.scores.league.positions[team.tla]
        league_table.append((
            league_pos,
            scores.league_points,
            scores.game_points,
            team.tla,
            team.name,
        ))

    # sort rows
    sort_col, sort_direction = SORT_TYPES[settings.sort]
    league_table.sort(key=lambda row: row[sort_col], reverse=sort_direction)

    # Print header
    print("Pos | League | Game | Team")
    for row in league_table:
        print(f"{row[0]:>3} | {row[1]:>6} | {row[2]:>4} | {row[3]+':':<5} {row[4]}")


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'show-league-table',
        help=__description__,
        description=__description__,
    )
    parser.add_argument(
        'compstate',
        help="competition state repo",
    )
    parser.add_argument(
        '--sort',
        choices=SORT_TYPES.keys(),
        default='position',
        help="Sort table by a column",
    )
    parser.set_defaults(func=command)
