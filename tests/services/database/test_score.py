import sqlite3

from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.services.database.score import save_all, load_all, create_table


def test_save_and_reload():
    scores = {
        '0ac6fc17cc544f3e97121a482e93ccf9': Score(tournament_points=3, victory_points=9, spice=2),
        'cb95a8863bfd48a487608c40ce4810ca': Score(solaris=7, water=1, troops_in_garrison=1),
        'ad0c20d4db874d9c9e47bd61bf077338': Score(),
    }

    with sqlite3.connect(":memory:") as database:
        cursor = database.cursor()
        create_table(cursor)
        save_all(cursor, round_=1, scores=scores)
        loaded_scores = load_all(cursor, round_=1)

    assert loaded_scores == scores
