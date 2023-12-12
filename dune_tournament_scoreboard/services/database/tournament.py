import atexit
import sqlite3
from pathlib import Path
from typing import Optional

from dune_tournament_scoreboard.assets.tournament import Tournament

DATA_ROOT = Path('data')
if not DATA_ROOT.exists():
    DATA_ROOT.mkdir(parents=True, exist_ok=True)

_connection: Optional[sqlite3.Connection] = None


def _connect(tournament_id: str):
    _disconnect()

    global _connection
    _connection = sqlite3.connect(DATA_ROOT / _get_file_name(tournament_id))


@atexit.register
def _disconnect():
    if _connection is not None:
        _connection.close()


def _get_file_name(name: str):
    return ''.join(c if c.isalnum() else '_' for c in name) + '.sql'


def create(tournament: Tournament):
    file_name = _get_file_name(tournament.id)
    for path in DATA_ROOT.glob('*.sql'):
        if path.name == file_name:
            raise ValueError(f"Tournament {tournament.id} already exists!")

    _connect(tournament.id)

    cursor = _connection.cursor()

    cursor.execute("CREATE TABLE tournament(id , )")



