import sqlite3
from itertools import count

from dune_tournament_scoreboard.assets.round import Round
from dune_tournament_scoreboard.services import database


def create_table(cursor: sqlite3.Cursor):
    database.table.create_table(cursor)
    database.score.create_table(cursor)


def save_all(cursor, rounds: list[Round]):
    for round_id, round_ in enumerate(rounds):
        save(cursor, round_id=round_id, round_=round_)


def save(cursor: sqlite3.Cursor, round_id: int, round_: Round):
    database.table.save_all(cursor, round_=round_id, tables=round_.tables)
    database.score.save_all(cursor, round_=round_id, scores=round_.scores)


def load_all(cursor: sqlite3.Cursor) -> list[Round]:
    rounds = []

    for round_id in count():
        tables = database.table.load_all(cursor, round_=round_id)
        if not tables:
            break
        scores = database.score.load_all(cursor, round_=round_id)
        rounds.append(Round(tables=tables, scores=scores))

    return rounds
