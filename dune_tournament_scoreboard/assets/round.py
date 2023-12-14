from typing import TypeAlias, Optional

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

    def compute_tournament_points(self, table: Optional[Table] = None):
        if table is None:
            for table in self.tables:
                self.compute_tournament_points(table)
            return

        player_order = sorted(table, key=lambda player_id_: self.scores.get(player_id_, Score()), reverse=True)

        for player_id, tournament_points in zip(player_order, [5, 3, 1]):
            self.scores[player_id].tournament_points = tournament_points

        for player_id in player_order[3:]:
            self.scores[player_id].tournament_points = 0
