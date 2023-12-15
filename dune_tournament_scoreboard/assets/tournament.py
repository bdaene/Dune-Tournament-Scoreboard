import random
from datetime import datetime, timezone
from itertools import permutations
from typing import TypeAlias

from attr import define, field

from dune_tournament_scoreboard.assets.player import PlayerId, Player
from dune_tournament_scoreboard.assets.round import Round, Table
from dune_tournament_scoreboard.assets.score import Score

TournamentId: TypeAlias = str


@define
class Tournament:
    id: TournamentId
    creation: datetime = field(factory=lambda: datetime.now(tz=timezone.utc))
    players: dict[PlayerId: Player] = field(factory=dict)
    rounds: list[Round] = field(factory=list)

    def update_player(self, player: Player):
        self.players[player.id] = player

    def deactivate_player(self, player: PlayerId):
        self.players[player].is_active = False

    def create_new_round(self):
        players = [player_id for player_id, player in self.players.items() if player.is_active]
        players.sort(key=lambda player_id: (self.get_total_score(player_id), random.random()), reverse=True)
        seats = _get_seats(self.rounds)
        tables = [_order_table(table, seats) for table in _create_tables(players)]
        self.rounds.append(Round(tables))

    def get_round(self, round_: int = -1):
        return self.rounds[round_]

    def get_total_score(self, player: PlayerId) -> Score:
        return sum((round_.scores.get(player, Score()) for round_ in self.rounds), start=Score())

    def get_tournament_points(self, player: PlayerId) -> list[int]:
        return [round_.scores.get(player, Score()).tournament_points for round_ in self.rounds]

    def get_summary(self) -> list[tuple[Player, list[int], Score]]:
        summary = [(player, self.get_tournament_points(player.id), self.get_total_score(player.id))
                   for player in self.players.values() if player.is_active]
        summary.sort(key=lambda line: line[-1], reverse=True)
        return summary


def _create_tables(players: list[PlayerId]) -> list[Table]:
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


def _get_seats(rounds: list[Round]) -> dict[PlayerId, list[int]]:
    seats = {}
    for round_ in rounds:
        for table in round_.tables:
            for seat, player in enumerate(table):
                seats.setdefault(player, []).append(seat)
    return seats


def _order_table(table: Table, previous_seats: dict[PlayerId, list[int]]) -> Table:
    possible_tables = [table_ for table_ in permutations(table)
                       if all(seat not in previous_seats[player] for seat, player in enumerate(table_))]

    if possible_tables:
        return list(random.choice(possible_tables))

    random.shuffle(table)
    return table
