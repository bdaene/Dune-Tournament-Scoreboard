import sqlite3
from itertools import groupby

from dune_tournament_scoreboard.assets.player import PlayerId
from dune_tournament_scoreboard.assets.round import Table


def create_table(cursor: sqlite3.Cursor):
    cursor.execute("""CREATE TABLE tables(
        round INTEGER NOT NULL,
        table_id INTEGER NOT NULL,
        seat INTEGER NOT NULL,
        player TEXT NOT NULL,
        
        UNIQUE (round, table_id, seat),
        
        PRIMARY KEY (round, table_id, seat),
        FOREIGN KEY (player) REFERENCES player(id)
    )""")


def save_all(cursor, round_: int, tables: list[Table]):
    for table, players in enumerate(tables):
        for seat, player in enumerate(players):
            save(cursor, round_, table, seat, player)


def save(cursor: sqlite3.Cursor, round_: int, table: int, seat: int, player: PlayerId):
    cursor.execute(
        """REPLACE INTO tables (round, table_id, seat, player) VALUES (:round, :table_id, :seat, :player)""",
        dict(round=round_, table_id=table, seat=seat, player=player)
    )


def load_all(cursor: sqlite3.Cursor, round_: int) -> list[Table]:
    seats = cursor.execute("""SELECT table_id, seat, player FROM tables WHERE round = :round""",
                           dict(round=round_, )).fetchall()

    return [[player for table, seat, player in group] for table, group in
            groupby(sorted(seats), lambda entry: entry[0])]
