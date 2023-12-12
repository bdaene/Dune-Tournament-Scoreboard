from dataclasses import dataclass

from dune_tournament_scoreboard.assets.player import Player
from dune_tournament_scoreboard.assets.score import Score


@dataclass
class Board:
    players: dict[str, Player]
    rounds: list[dict[str, Score]]

    def get_total_score(self, player: Player) -> Score:
        score = Score()
        for round_scores in self.rounds:
            score += round_scores.get(player.id, Score())
        return score

    def get_tournament_points(self, player: Player) -> list[int]:
        return [round_scores.get(player.id, Score()).tournament_points for round_scores in self.rounds]

    def get_summary(self) -> list[tuple[Player, list[int], Score]]:
        summary = [(player, self.get_tournament_points(player), self.get_total_score(player))
                   for player in self.players.values()]
        summary.sort(key=lambda line: line[-1], reverse=True)
        return summary

    def get_tables(self) -> list[list[Player]]:
        players = sorted(self.players.values(), key=self.get_total_score, reverse=True)

        if len(players) < 5:
            return [players]
        if len(players) == 5:
            return [players[:3], players[3:]]

        table_of_3 = (3 * len(players)) % 4
        table_of_4 = (len(players) - table_of_3 * 3) // 4

        tables = []
        offset = 0
        for table in range(table_of_4):
            tables.append(players[offset:offset + 4])
            offset += 4
        for table in range(table_of_3):
            tables.append(players[offset:offset + 3])
            offset += 3

        return tables
