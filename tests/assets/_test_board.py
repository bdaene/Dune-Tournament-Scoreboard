import pytest

from dune_tournament_scoreboard.assets._board import Board
from dune_tournament_scoreboard.assets.player import Player
from dune_tournament_scoreboard.assets.score import Score

PLAYERS = [Player(id=name, name=name.upper(), surname=name.title()) for name in "abcdefghij"]


def _get_test_board():
    return Board(
        players={player.id: player for player in PLAYERS},
        rounds=[
            {
                PLAYERS[0].id: Score(0, 0, 6, 8, 1, 2),
                PLAYERS[1].id: Score(9, 3, 3, 9, 4, 5),
                PLAYERS[5].id: Score(9, 3, 0, 6, 9, 1),
                PLAYERS[7].id: Score(7, 1, 0, 0, 6, 3),
            },
            {
                PLAYERS[0].id: Score(6, 9, 6, 0, 2, 9),
                PLAYERS[2].id: Score(9, 7, 1, 8, 1, 8),
                PLAYERS[3].id: Score(4, 8, 1, 6, 8, 2),
                PLAYERS[7].id: Score(6, 8, 8, 4, 8, 5),
            },
            {
                PLAYERS[0].id: Score(8, 7, 7, 2, 9, 9),
                PLAYERS[4].id: Score(9, 8, 7, 5, 5, 4),
                PLAYERS[5].id: Score(6, 0, 5, 6, 3, 1),
                PLAYERS[8].id: Score(6, 2, 7, 9, 0, 4),
            }
        ]
    )


@pytest.mark.parametrize("player, expected_score", [
    (PLAYERS[0], Score(14, 16, 19, 10, 12, 20)),
    (PLAYERS[1], Score(9, 3, 3, 9, 4, 5)),
    (PLAYERS[5], Score(15, 3, 5, 12, 12, 2)),
    (PLAYERS[8], Score(6, 2, 7, 9, 0, 4)),
])
def test_get_total_score(player, expected_score):
    assert _get_test_board().get_total_score(player) == expected_score


@pytest.mark.parametrize("player, expected_points", [
    (PLAYERS[0], [0, 6, 8]),
    (PLAYERS[5], [9, 0, 6]),
    (PLAYERS[3], [0, 4, 0]),
])
def test_get_tournament_points(player, expected_points):
    assert _get_test_board().get_tournament_points(player) == expected_points


@pytest.mark.parametrize("board, expected_summary", [
    (_get_test_board(), [
        (PLAYERS[5], [9, 0, 6], Score(15, 3, 5, 12, 12, 2)),
        (PLAYERS[0], [0, 6, 8], Score(14, 16, 19, 10, 12, 20)),
        (PLAYERS[7], [7, 6, 0], Score(13, 9, 8, 4, 14, 8)),
        (PLAYERS[4], [0, 0, 9], Score(9, 8, 7, 5, 5, 4)),
        (PLAYERS[2], [0, 9, 0], Score(9, 7, 1, 8, 1, 8)),
        (PLAYERS[1], [9, 0, 0], Score(9, 3, 3, 9, 4, 5)),
        (PLAYERS[8], [0, 0, 6], Score(6, 2, 7, 9, 0, 4)),
        (PLAYERS[3], [0, 4, 0], Score(4, 8, 1, 6, 8, 2)),
        (PLAYERS[6], [0, 0, 0], Score(0, 0, 0, 0, 0, 0)),
        (PLAYERS[9], [0, 0, 0], Score(0, 0, 0, 0, 0, 0))
    ]),
])
def test_get_summary(board, expected_summary):
    assert board.get_summary() == expected_summary


@pytest.mark.parametrize("board, expected_tables", [
    (_get_test_board(), [
        [PLAYERS[5], PLAYERS[0], PLAYERS[7], PLAYERS[4]],
        [PLAYERS[2], PLAYERS[1], PLAYERS[8]],
        [PLAYERS[3], PLAYERS[6], PLAYERS[9]],
    ]),
])
def test_get_tables(board, expected_tables):
    assert board.get_tables() == expected_tables
