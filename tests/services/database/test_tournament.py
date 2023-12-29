import sqlite3

import pytest

from dune_tournament_scoreboard.assets.player import Player
from dune_tournament_scoreboard.assets.round import Round
from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.assets.tournament import Tournament
from dune_tournament_scoreboard.services.database.tournament import (save, load, create_table, create, list_all, select)


def test_save_and_reload():
    tournament = Tournament(
        id="tournament",
        players={
            'a': Player(id='a', name="A", surname="a"),
            'b': Player(id='b', name="B", surname="b"),
        },
        rounds=[
            Round(
                tables=[["a", "b"], ["c"]],
                scores={"a": Score(tournament_points=5)}
            ),
            Round(
                tables=[["a"]],
            )
        ]
    )

    with sqlite3.connect(":memory:") as database:
        cursor = database.cursor()
        create_table(cursor)
        save(cursor, tournament=tournament)
        loaded_tournament = load(cursor)

    assert loaded_tournament == tournament


def test_create_list_and_select(temporary_data_root):
    assert list_all() == []

    tournament_a = Tournament(id="a")
    tournament_b = Tournament(id="b")
    tournament_c = Tournament(id="c")

    create(tournament_a),
    create(tournament_c),

    assert list_all() == ["a", "c"]

    with pytest.raises(ValueError):
        select("b")

    create(tournament_b)
    with pytest.raises(ValueError):
        create(tournament_b)

    assert select("a") == tournament_a
