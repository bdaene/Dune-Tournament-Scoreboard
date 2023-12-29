import sqlite3
from typing import Iterable

from dune_tournament_scoreboard.assets.player import Player


def create_table(cursor: sqlite3.Cursor):
    cursor.execute("""CREATE TABLE player(
        id TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        is_active INTEGER NOT NULL,
        
        UNIQUE (name, surname),
        UNIQUE (id),
        
        PRIMARY KEY (id)
    )""")


def save_all(cursor, players: Iterable[Player]):
    for player in players:
        save(cursor, player)


def save(cursor: sqlite3.Cursor, player: Player):
    cursor.execute(
        """REPLACE INTO player (id, name, surname, is_active) VALUES (:id, :name, :surname, :is_active)""",
        dict(id=player.id, name=player.name, surname=player.surname, is_active=player.is_active)
    )


def load_all(cursor: sqlite3.Cursor) -> list[Player]:
    players = cursor.execute("""SELECT id, name, surname, is_active FROM player""").fetchall()
    return [Player(id=player_id, name=name, surname=surname, is_active=is_active)
            for player_id, name, surname, is_active in players]
