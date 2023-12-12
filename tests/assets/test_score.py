import pytest

from dune_tournament_scoreboard.assets.score import Score


@pytest.mark.parametrize("lower_score, upper_score", [
    (Score(4, 8, 3, 2, 4, 1), Score(9, 5, 3, 4, 1, 2)),
    (Score(4, 8, 3, 2, 4, 1), Score(4, 8, 3, 2, 4, 2)),
    (Score(9, 8, 3, 2, 4, 1), Score(10, 9, 3, 2, 4, 2)),
])
def test_order(lower_score, upper_score):
    assert lower_score < upper_score
    assert upper_score > lower_score


@pytest.mark.parametrize("score_1, score_2, expected_score", [
    (Score(), Score(), Score()),
    (Score(), Score(5, 7, 2, 3, 6, 4), Score(5, 7, 2, 3, 6, 4)),
    (Score(5, 7, 2, 3, 6, 4), Score(), Score(5, 7, 2, 3, 6, 4)),
    (Score(9, 1, 7, 2, 6, 1), Score(0, 3, 1, 3, 2, 4), Score(9, 4, 8, 5, 8, 5)),
])
def test_add(score_1, score_2, expected_score):
    assert score_1 + score_2 == expected_score
