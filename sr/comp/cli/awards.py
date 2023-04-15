from __future__ import annotations

import argparse

from sr.comp.types import TLA


def command(settings: argparse.Namespace) -> None:
    import os.path

    from sr.comp.comp import SRComp
    from sr.comp.winners import Award

    comp = SRComp(os.path.realpath(settings.compstate))

    def format_team(tla: TLA) -> str:
        team = comp.teams[tla]
        return '{} ({}{})'.format(
            tla,
            team.name,
            ' [rookie]' if team.rookie else '',
        )

    award_order = (
        Award.image,
        Award.web,
        Award.committee,
        Award.rookie,
        Award.movement,
        Award.third,
        Award.second,
        Award.first,
    )

    missing = set(Award) - set(award_order)
    assert not missing, "Awards missed!: {}".format(", ".join(map(str, missing)))

    for award in award_order:
        print(f'### {award.value.upper()}')
        recipients = comp.awards.get(award, None)
        if recipients is None:
            print('  Not yet awarded.')
        elif not recipients:
            print('  Awarded to nobody.')
        elif len(recipients) == 1:
            print(" ", format_team(recipients[0]))
        else:
            print(f'  Split between {len(recipients)} teams (a tie):')
            for recipient in recipients:
                print("  ", format_team(recipient))
        print()


def add_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    help_msg = "Show who has been given awards."
    parser = subparsers.add_parser(
        'awards',
        help=help_msg,
        description=help_msg,
    )
    parser.add_argument('compstate', help="competition state repo")
    parser.set_defaults(func=command)
