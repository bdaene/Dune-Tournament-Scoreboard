from typing import TypeAlias

from attrs import define, field

from dune_tournament_scoreboard.assets.player import PlayerId
from dune_tournament_scoreboard.assets.score import Score

Table: TypeAlias = list[PlayerId]


@define
class Round:
    tables: list[Table]
    scores: dict[PlayerId: Score] = field(factory=dict)
