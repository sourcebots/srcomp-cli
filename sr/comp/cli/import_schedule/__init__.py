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
from pathlib import Path

from sr.comp.cli.import_schedule import loading, teams_mapping
from sr.comp.cli.import_schedule.types import Configuration


def get_configuration(
    compensate_path: Path,
    team_order_strategy: teams_mapping.Strategy,
) -> Configuration:
    # Grab the teams and arenas
    try:
        team_ids, arena_ids, teams_per_game = loading.load_teams_areans(compensate_path)
    except Exception as e:
        print("Failed to load existing state ({0}).".format(e))
        print("Make it valid (consider removing the league.yaml and layout.yaml)")
        print("and try again.")
        exit(1)

    # Semi-randomise
    team_ids = teams_mapping.order_teams(
        compensate_path,
        team_ids,
        team_order_strategy,
    )

    return Configuration(
        arena_ids,
        team_ids,
        teams_per_game,
    )


def command(args: argparse.Namespace) -> None:
    from sr.comp.cli.import_schedule import core

    with open(args.schedule, 'r') as sfp:
        schedule_lines = loading.tidy(sfp.readlines())

    config = get_configuration(
        args.compstate,
        args.team_order_strategy,
    )

    matches, bad_matches = core.build_schedule(
        config,
        schedule_lines,
        args.ignore_ids,
    )

    # Print any warnings about the matches
    for bad_match in bad_matches:
        print(
            f"Warning: match {bad_match.arena}:{bad_match.num} only has "
            f"{bad_match.num_teams} teams.",
        )

    # Save the matches to the file
    league_yaml = loading.league_yaml_path(args.compstate)
    loading.dump_league_yaml(matches, league_yaml)


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
        type=loading.parse_ids,
        help="comma separated list of ids to ignore",
    )
    parser.add_argument(
        '--extend',
        default=False,
        action='store_true',
        help=(
            "Whether to replace (the defualt) or extend the existing league "
            "with the matches in the given schedule file."
        ),
    )
    parser.add_argument(
        '--team-order-strategy',
        choices=teams_mapping.Strategy,
        default=teams_mapping.Strategy.AUTO,
        type=teams_mapping.Strategy,
        help="How to map schedule ids to TLAs",
    )
    parser.add_argument('compstate', type=Path, help="competition state repository")
    parser.add_argument('schedule', type=Path, help="schedule to import")
    parser.set_defaults(func=command)
