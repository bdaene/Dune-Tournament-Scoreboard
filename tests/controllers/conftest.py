import pytest

from dune_tournament_scoreboard import controllers
from dune_tournament_scoreboard.assets.player import Player
from dune_tournament_scoreboard.assets.round import Round
from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.assets.tournament import Tournament


def _get_test_tournament():
    players = [Player(id=name, name=name.upper(), surname=name.title()) for name in "abcdefghijk"]
    players[-3].is_active = False

    return Tournament(
        id="tournament",
        players={player.id: player for player in players},
        rounds=[
            Round(
                tables=[
                    ['a', 'b', 'f', 'h'],
                    ['i', 'c', 'g', 'j'],
                    ['d', 'e', 'k']
                ],
                scores={
                    'a': Score(0, 0, 6, 8, 1, 2),
                    'b': Score(9, 3, 3, 9, 4, 5),
                    'f': Score(9, 3, 0, 6, 9, 1),
                    'g': Score(7, 1, 0, 0, 6, 3),
                }
            ),
            Round(
                tables=[
                    ['b', 'a', 'h', 'f'],
                    ['c', 'g', 'e', 'd'],
                    ['k', 'j', 'i']
                ],
                scores={
                    'a': Score(6, 9, 6, 0, 2, 9),
                    'c': Score(9, 7, 1, 8, 1, 8),
                    'd': Score(4, 8, 1, 6, 8, 2),
                    'h': Score(6, 8, 8, 4, 8, 5),
                }
            ),
            Round(
                tables=[
                    ['f', 'h', 'b', 'c'],
                    ['j', 'd', 'a'],
                    ['e', 'g', 'k']
                ],
                scores={
                    'a': Score(1, 7, 7, 2, 9, 9),
                    'e': Score(9, 8, 7, 5, 5, 4),
                    'f': Score(6, 0, 5, 6, 3, 1),
                    'g': Score(6, 2, 7, 9, 0, 4),
                }
            ),
        ]
    )


@pytest.fixture
def reset_current_tournament():
    controllers.tournament._current_tournament = _get_test_tournament()


@pytest.fixture
def unselect_current_tournament():
    controllers.tournament._current_tournament = None
