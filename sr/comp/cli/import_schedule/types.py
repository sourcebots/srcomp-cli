from typing import Dict, List, NamedTuple, NewType, Optional, TypeVar

from sr.comp.types import ArenaName, MatchNumber, TLA

T = TypeVar('T')
ID = NewType('ID', str)
RawMatch = Dict[ArenaName, List[Optional[TLA]]]


class BadMatch(NamedTuple):
    arena: ArenaName
    num: MatchNumber
    num_teams: int
