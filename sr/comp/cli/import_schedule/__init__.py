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

from sr.comp.cli.import_schedule import loading


def command(args: argparse.Namespace) -> None:
    from sr.comp.cli.import_schedule import core, teams_mapping

    with open(args.schedule, 'r') as sfp:
        schedule_lines = loading.tidy(sfp.readlines())

    # Grab the teams and arenas
    try:
        team_ids, arena_ids, teams_per_game = loading.load_teams_areans(args.compstate)
    except Exception as e:
        print("Failed to load existing state ({0}).".format(e))
        print("Make it valid (consider removing the league.yaml and layout.yaml)")
        print("and try again.")
        exit(1)

    # Semi-randomise
    team_ids = teams_mapping.order_teams(args.compstate, team_ids)

    matches, bad_matches = core.build_schedule(
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
    parser.add_argument('compstate', type=Path, help="competition state repository")
    parser.add_argument('schedule', type=Path, help="schedule to import")
    parser.set_defaults(func=command)
