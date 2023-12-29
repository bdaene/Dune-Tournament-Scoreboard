import pytest

from dune_tournament_scoreboard.assets.round import Round
from dune_tournament_scoreboard.assets.tournament import Tournament
from dune_tournament_scoreboard.assets.player import Player
from dune_tournament_scoreboard.assets.score import Score

PLAYERS = [Player(id=name, name=name.upper(), surname=name.title()) for name in "abcdefghij"]


def _get_test_tournament():
    return Tournament(
        id="tournament",
        players={player.id: player for player in PLAYERS},
        rounds=[
            Round(
                tables=[[PLAYERS[0].id, PLAYERS[1].id], [PLAYERS[5].id, PLAYERS[7].id]],
                scores={
                    PLAYERS[0].id: Score(0, 0, 6, 8, 1, 2),
                    PLAYERS[1].id: Score(9, 3, 3, 9, 4, 5),
                    PLAYERS[5].id: Score(9, 3, 0, 6, 9, 1),
                    PLAYERS[7].id: Score(7, 1, 0, 0, 6, 3),
                }
            ),
            Round(
                tables=[[PLAYERS[0].id, PLAYERS[2].id], [PLAYERS[3].id, PLAYERS[7].id]],
                scores={
                    PLAYERS[0].id: Score(6, 9, 6, 0, 2, 9),
                    PLAYERS[2].id: Score(9, 7, 1, 8, 1, 8),
                    PLAYERS[3].id: Score(4, 8, 1, 6, 8, 2),
                    PLAYERS[7].id: Score(6, 8, 8, 4, 8, 5),
                }
            ),
            Round(
                tables=[[PLAYERS[0].id, PLAYERS[4].id], [PLAYERS[5].id, PLAYERS[8].id]],
                scores={
                    PLAYERS[0].id: Score(8, 7, 7, 2, 9, 9),
                    PLAYERS[4].id: Score(9, 8, 7, 5, 5, 4),
                    PLAYERS[5].id: Score(6, 0, 5, 6, 3, 1),
                    PLAYERS[8].id: Score(6, 2, 7, 9, 0, 4),
                }
            )
        ]
    )


@pytest.mark.parametrize("player, expected_score", [
    (PLAYERS[0].id, Score(14, 16, 19, 10, 12, 20)),
    (PLAYERS[1].id, Score(9, 3, 3, 9, 4, 5)),
    (PLAYERS[5].id, Score(15, 3, 5, 12, 12, 2)),
    (PLAYERS[8].id, Score(6, 2, 7, 9, 0, 4)),
])
def test_get_total_score(player, expected_score):
    assert _get_test_tournament().get_total_score(player) == expected_score


@pytest.mark.parametrize("player, expected_points", [
    (PLAYERS[0].id, [0, 6, 8]),
    (PLAYERS[5].id, [9, 0, 6]),
    (PLAYERS[3].id, [0, 4, 0]),
])
def test_get_tournament_points(player, expected_points):
    assert _get_test_tournament().get_tournament_points(player) == expected_points


@pytest.mark.parametrize("tournament, expected_summary", [
    (_get_test_tournament(), [
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
def test_get_summary(tournament, expected_summary):
    assert tournament.get_summary() == expected_summary


@pytest.mark.parametrize("tournament, expected_tables", [
    (_get_test_tournament(), [
        [PLAYERS[0].id, PLAYERS[4].id, PLAYERS[5].id, PLAYERS[7].id],
        [PLAYERS[1].id, PLAYERS[2].id, PLAYERS[8].id],
        [PLAYERS[3].id, PLAYERS[6].id, PLAYERS[9].id],
    ]),
])
def test_create_new_round(tournament, expected_tables):
    tournament.create_new_round()
    assert list(map(sorted, tournament.get_round().tables)) == expected_tables


def test_update_player():
    tournament = _get_test_tournament()
    tournament.update_player(Player(id='1', name="hello", surname="world"))
    assert tournament.players['1'] == Player(id='1', name="hello", surname="world")


def test_deactivate_player():
    tournament = _get_test_tournament()
    tournament.deactivate_player('f')
    assert not tournament.players['f'].is_active
