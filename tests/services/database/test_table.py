import sqlite3

from dune_tournament_scoreboard.services.database.table import save_all, load_all, create_table


def test_save_and_reload():
    tables = [
        ["a", "b", "c", "d"],
        ["dq4411za", "w64qz64", "qdz6486"],
        ["54211", "54413", "42134"],
    ]

    with sqlite3.connect(":memory:") as database:
        cursor = database.cursor()
        create_table(cursor)
        save_all(cursor, round_=3, tables=tables)
        loaded_tables = load_all(cursor, round_=3)

    assert loaded_tables == tables
