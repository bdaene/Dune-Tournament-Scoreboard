from typing import TypeAlias

from attr import define, field

from dune_tournament_scoreboard.assets.player import PlayerId
from dune_tournament_scoreboard.assets.score import Score

Table: TypeAlias = list[PlayerId]


@define
class Round:
    tables: list[Table]
    scores: dict[PlayerId: Score] = field(factory=dict)

    def update_score(self, player: PlayerId, score: Score):
        self.scores[player] = score

    def get_score(self, player: PlayerId) -> Score:
        return self.scores.get(player, Score())
