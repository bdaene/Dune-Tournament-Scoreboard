import sqlite3

from dune_tournament_scoreboard.assets.player import Player
from dune_tournament_scoreboard.services.database.player import save_all, load_all, create_table


def test_save_and_reload():
    players = [
        Player(name="A", surname="a"),
        Player(name="B", surname="b", is_active=False),
        Player(name="C", surname="fqiq@4678&#"),
    ]

    with sqlite3.connect(":memory:") as database:
        cursor = database.cursor()
        create_table(cursor)
        save_all(cursor, players)
        loaded_players = load_all(cursor)

    assert loaded_players == players
