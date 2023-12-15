from functools import wraps
from typing import Optional

from dune_tournament_scoreboard.assets.player import Player, PlayerId
from dune_tournament_scoreboard.assets.round import Table
from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.assets.tournament import Tournament, TournamentId

_current_tournament: Optional[Tournament] = None


def check_current_tournament(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _current_tournament is None:
            raise ValueError("No tournament selected!")
        func(*args, **kwargs)

    return wrapper


def create(id_: TournamentId):
    tournament = Tournament(id=id_)
    # TODO save new tournament in DB

    global _current_tournament
    _current_tournament = tournament


def select(id_: TournamentId):
    tournament = Tournament(id=id_)  # TODO load tournament from DB

    global _current_tournament
    _current_tournament = tournament


def get_current() -> Optional[TournamentId]:
    if _current_tournament is None:
        return None
    return _current_tournament.id


def list_tournaments() -> list[TournamentId]:
    return []  # TODO fetch tournaments from DB


@check_current_tournament
def create_player(name: str, surname: str):
    player = Player(name=name, surname=surname)
    _current_tournament.update_player(player)
    # TODO: save player


@check_current_tournament
def list_players() -> list[Player]:
    return list(_current_tournament.players.values())


@check_current_tournament
def update_player(player: Player):
    _current_tournament.update_player(player)
    # TODO: save player


@check_current_tournament
def deactivate_player(player: PlayerId):
    _current_tournament.deactivate_player(player)
    # TODO: save player


@check_current_tournament
def create_round():
    _current_tournament.create_new_round()
    # TODO: save new round tables


@check_current_tournament
def list_tables(round_: int = -1) -> list[Table]:
    return _current_tournament.get_round(round_).tables


@check_current_tournament
def update_score(player: PlayerId, score: Score, round_: int = -1):
    _current_tournament.get_round(round_).update_score(player, score)
    # TODO: save updated score


@check_current_tournament
def get_score(player: PlayerId, round_: int = -1):
    _current_tournament.get_round(round_).get_score(player)


@check_current_tournament
def get_scores(round_: int = -1, table: int = None) -> list[list[tuple[PlayerId, Score]]]:
    round_ = _current_tournament.get_round(round_)
    if table is None:
        tables = round_.tables
    else:
        tables = [round_.tables[table]]

    return [[(player, round_.get_score(player)) for player in table] for table in tables]


@check_current_tournament
def compute_tournament_points(round_: int = -1, table: int = None):
    round_ = _current_tournament.get_round(round_)
    if table is None:
        tables = round_.tables
    else:
        tables = [round_.tables[table]]

    for table in tables:
        round_.compute_tournament_points(table)
    # TODO save updated scores


@check_current_tournament
def get_summary() -> list[tuple[Player, list[int], Score]]:
    return _current_tournament.get_summary()
