"""Show the current state of the league table"""


SORT_TYPES = {  # cli string: (sort column, sort direction)
    'rank': (0, False),
    'game': (2, True),
    'team': (3, False),
}


def command(settings):
    import os.path
    from collections import Counter

    from tabulate import tabulate

    from sr.comp.comp import SRComp

    comp = SRComp(os.path.realpath(settings.compstate))

    tie_count = Counter(comp.scores.league.positions.values())
    tied_positions = set(x for x, y in tie_count.items() if y > 1)

    league_table = []
    for team in comp.teams.values():
        scores = comp.scores.league.teams[team.tla]
        league_pos = comp.scores.league.positions[team.tla]
        league_table.append([
            league_pos,
            scores.league_points,
            scores.game_points,
            team.tla,
            team.name,
        ])

    # sort rows
    sort_col, sort_direction = SORT_TYPES[settings.sort]
    league_table.sort(key=lambda row: row[sort_col], reverse=sort_direction)

    # apply tie formatting
    for team_data in league_table:
        if team_data[0] in tied_positions:
            team_data[0] = f"={team_data[0]}"

    # Print table
    print(tabulate(
        [
            [rank, league_points, game_points, f"{tla}: {team_name}"]
            for rank, league_points, game_points, tla, team_name in league_table
        ],
        headers=["Rank", "League", "Game", "Team"],
        tablefmt='github',
        colalign=('center', 'center', 'center', 'left'),  # left-align team names
    ))


def add_subparser(subparsers):
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
