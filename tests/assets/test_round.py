from dune_tournament_scoreboard.assets.round import Round
from dune_tournament_scoreboard.assets.score import Score


def test_update_and_get_score():
    round_ = Round(
        tables=[]
    )

    assert round_.scores == {}

    round_.update_score("a", Score(tournament_points=5))

    assert round_.get_score("a") == Score(tournament_points=5)
    assert round_.get_score("b") == Score()
