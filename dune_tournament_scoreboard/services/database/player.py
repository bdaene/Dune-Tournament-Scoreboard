import sqlite3
from typing import Iterable

from dune_tournament_scoreboard.assets import Player
from dune_tournament_scoreboard.assets.player import PlayerId


def create_table(cursor: sqlite3.Cursor):
    cursor.execute("""CREATE TABLE player(
        id TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL, 
        surname TEXT NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (name, surname)
    )""")


def save_all(cursor, players: dict[PlayerId, Player]):
    for player in players.values():
        save(cursor, player)


def save(cursor: sqlite3.Cursor, player: Player):
    cursor.execute(
        """REPLACE INTO player (id, name, surname) VALUES (?,?,?)""",
        (player.id, player.name, player.surname)
    )


def load_all(cursor: sqlite3.Cursor) -> dict[PlayerId, Player]:
    players = cursor.execute("""SELECT id, name, surname FROM player""").fetchall()
    return {player_id: Player(id=player_id, name=name, surname=surname) for player_id, name, surname in players}
