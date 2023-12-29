import random
from functools import wraps
from itertools import permutations
from typing import Optional

from dune_tournament_scoreboard.assets.player import Player, PlayerId
from dune_tournament_scoreboard.assets.round import Table, Round
from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.assets.tournament import Tournament, TournamentId
from dune_tournament_scoreboard.services import database

_current_tournament: Optional[Tournament] = None


def _check_current_tournament(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _current_tournament is None:
            raise ValueError("No tournament selected!")
        return func(*args, **kwargs)

    return wrapper


def create(tournament_id: TournamentId):
    tournament = Tournament(id=tournament_id)

    database.tournament.create(tournament=tournament)

    global _current_tournament
    _current_tournament = tournament


def select(tournament_id: TournamentId):
    tournament = database.tournament.select(tournament_id=tournament_id)

    global _current_tournament
    _current_tournament = tournament


def get_current() -> Optional[TournamentId]:
    if _current_tournament is None:
        return None
    return _current_tournament.id


def list_tournaments() -> list[TournamentId]:
    return database.tournament.list_all()


def create_player(name: str, surname: str) -> PlayerId:
    player = Player(name=name, surname=surname)
    update_player(player)
    return player.id


@_check_current_tournament
def get_player(player_id: PlayerId) -> Optional[Player]:
    return _current_tournament.players.get(player_id)


@_check_current_tournament
def list_players() -> list[Player]:
    return sorted(_current_tournament.players.values(),
                  key=lambda player: (player.name.upper(), player.surname.title()))


@_check_current_tournament
def update_player(player: Player):
    _current_tournament.players[player.id] = player

    database.player.save(database.tournament.get_cursor(), player=player)
    database.tournament.commit()


@_check_current_tournament
def deactivate_player(player: PlayerId):
    _current_tournament.players[player].is_active = False

    database.player.save(database.tournament.get_cursor(), player=_current_tournament.players[player])
    database.tournament.commit()


@_check_current_tournament
def create_new_round():
    rounds = _current_tournament.rounds
    round_id = len(rounds)

    players = [player_id for player_id, player in _current_tournament.players.items() if player.is_active]
    players.sort(key=lambda player_id: (_get_total_score(player_id, rounds), random.random()), reverse=True)
    seats = _get_seats(rounds)
    tables = [_order_table(table, seats) for table in _create_tables(players)]
    rounds.append(Round(tables))

    database.table.save_all(database.tournament.get_cursor(), round_=round_id,
                            tables=_current_tournament.rounds[round_id].tables)
    database.tournament.commit()


@_check_current_tournament
def list_tables(round_: int = -1) -> list[Table]:
    try:
        return _current_tournament.rounds[round_].tables
    except IndexError:
        return []


@_check_current_tournament
def update_score(player: PlayerId, score: Score, round_: int = -1):
    _current_tournament.rounds[round_].scores[player] = score

    if round_ < 0:
        round_ = len(_current_tournament.rounds) + round_

    database.score.save(database.tournament.get_cursor(), round_=round_, player_id=player, score=score)
    database.tournament.commit()


@_check_current_tournament
def get_score(player: PlayerId, round_: int = -1):
    return _current_tournament.rounds[round_].scores.get(player, Score())


@_check_current_tournament
def get_summary() -> list[tuple[Player, list[int], Score]]:
    rounds = _current_tournament.rounds
    summary = [(player, _get_tournament_points(player.id, rounds), _get_total_score(player.id, rounds))
               for player in _current_tournament.players.values()]
    summary.sort(key=lambda line: line[-1], reverse=True)
    return summary


def _get_total_score(player: PlayerId, rounds: list[Round]) -> Score:
    return sum((round_.scores.get(player, Score()) for round_ in rounds), start=Score())


def _get_tournament_points(player: PlayerId, rounds: list[Round]) -> list[int]:
    return [round_.scores[player].tournament_points if player in round_.scores else None for round_ in rounds]


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
                       if all(seat not in previous_seats.get(player, []) for seat, player in enumerate(table_))]

    if possible_tables:
        return list(random.choice(possible_tables))

    random.shuffle(table)
    return table
