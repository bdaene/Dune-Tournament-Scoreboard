import sqlite3

from dune_tournament_scoreboard.assets.round import Round
from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.services.database.round import save_all, load_all, create_table


def test_save_and_reload():
    rounds = [
        Round(
            tables=[
                ["a", "b", "c", "d"]
            ],
            scores={
                "a": Score(tournament_points=5),
                "b": Score(tournament_points=3),
                "c": Score()
            }
        ),
        Round(
            tables=[
                ["e", "c", "a", "b"]
            ],
            scores={
                "c": Score(tournament_points=5),
                "b": Score(tournament_points=3),
            }
        ),

    ]

    with sqlite3.connect(":memory:") as database:
        cursor = database.cursor()
        create_table(cursor)
        save_all(cursor, rounds)
        loaded_rounds = load_all(cursor)

    assert loaded_rounds == rounds
