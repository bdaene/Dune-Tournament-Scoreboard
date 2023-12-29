import atexit
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from dune_tournament_scoreboard.assets.tournament import Tournament, TournamentId
from dune_tournament_scoreboard.services import database

DATA_ROOT = Path('data')
if not DATA_ROOT.exists():
    DATA_ROOT.mkdir(parents=True, exist_ok=True)

_connection: Optional[sqlite3.Connection] = None


def _get_file_name(tournament_id: TournamentId):
    return ''.join(c if c.isalnum() else '_' for c in tournament_id) + '.db'


def _check_exists(tournament_id) -> bool:
    file_name = _get_file_name(tournament_id)
    for path in DATA_ROOT.glob('*.db'):
        if path.name == file_name:
            return True
    return False


def _connect(tournament_id: TournamentId):
    _disconnect()

    global _connection
    _connection = sqlite3.connect(DATA_ROOT / _get_file_name(tournament_id))


@atexit.register
def _disconnect():
    global _connection
    if _connection is not None:
        _connection.close()
    _connection = None


def list_all() -> list[TournamentId]:
    return sorted(path.stem for path in DATA_ROOT.glob('*.db'))


def select(tournament_id) -> Tournament:
    if not _check_exists(tournament_id):
        raise ValueError(f"Tournament {tournament_id} does not exists!")

    _connect(tournament_id)
    cursor = get_cursor()
    return load(cursor)


def get_cursor():
    if _connection is None:
        raise ValueError("No tournament selected.")
    return _connection.cursor()


def commit():
    if _connection is None:
        raise ValueError("No tournament selected.")
    return _connection.commit()


def create(tournament: Tournament):
    if _check_exists(tournament.id):
        raise ValueError(f"Tournament {tournament.id} already exists!")

    _connect(tournament.id)
    cursor = get_cursor()

    create_table(cursor)
    save(cursor, tournament)
    commit()


def create_table(cursor: sqlite3.Cursor):
    cursor.execute("""CREATE TABLE tournament(
        id TEXT NOT NULL,
        creation DATETIME NOT NULL,

        UNIQUE (id)

        PRIMARY KEY (id)
    )""")

    database.player.create_table(cursor)
    database.round.create_table(cursor)


def save(cursor: sqlite3.Cursor, tournament: Tournament):
    cursor.execute("""REPLACE INTO tournament (id, creation) VALUES (:id, :creation)""",
                   dict(id=tournament.id, creation=tournament.creation.isoformat()))
    database.player.save_all(cursor, players=tournament.players.values())
    database.round.save_all(cursor, rounds=tournament.rounds)


def load(cursor: sqlite3.Cursor) -> Tournament:
    tournament_id, creation = cursor.execute("""SELECT id, creation FROM tournament""").fetchone()
    players = {player.id: player for player in database.player.load_all(cursor)}
    rounds = database.round.load_all(cursor)

    return Tournament(
        id=tournament_id,
        creation=datetime.fromisoformat(creation),
        players=players,
        rounds=rounds,
    )
