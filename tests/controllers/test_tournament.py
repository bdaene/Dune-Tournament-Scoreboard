from unittest import mock

from dune_tournament_scoreboard.assets.player import Player
from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.assets.tournament import Tournament
from dune_tournament_scoreboard.controllers.tournament import (get_summary, create_new_round, list_tables, get_player,
                                                               create, get_current, select, list_tournaments,
                                                               create_player, update_player, deactivate_player,
                                                               list_players, get_score, update_score)


def test_get_summary(reset_current_tournament):
    assert get_summary() == [
        (get_player('f'), [9, 0, 6], Score(15, 3, 5, 12, 12, 2)),
        (get_player('g'), [7, 0, 6], Score(13, 3, 7, 9, 6, 7)),
        (get_player('e'), [0, 0, 9], Score(9, 8, 7, 5, 5, 4)),
        (get_player('c'), [0, 9, 0], Score(9, 7, 1, 8, 1, 8)),
        (get_player('b'), [9, 0, 0], Score(9, 3, 3, 9, 4, 5)),
        (get_player('a'), [0, 6, 1], Score(7, 16, 19, 10, 12, 20)),
        (get_player('h'), [0, 6, 0], Score(6, 8, 8, 4, 8, 5)),
        (get_player('d'), [0, 4, 0], Score(4, 8, 1, 6, 8, 2)),
        (get_player('j'), [0, 0, 0], Score(0, 0, 0, 0, 0, 0)),
        (get_player('k'), [0, 0, 0], Score(0, 0, 0, 0, 0, 0)),
    ]


@mock.patch('dune_tournament_scoreboard.controllers.tournament.database')
def test_create_new_round(database_mock, reset_current_tournament):
    expected_tables = [
        ['c', 'e', 'f', 'g'],
        ['a', 'b', 'h'],
        ['d', 'j', 'k'],
    ]
    create_new_round()

    assert list(map(sorted, list_tables())) == expected_tables
    database_mock.table.save_all.assert_called_with(mock.ANY, round_=3, tables=list_tables())


@mock.patch('dune_tournament_scoreboard.controllers.tournament.database')
def test_create(database_mock):
    create(tournament_id="Test tournament")

    assert get_current() == "Test tournament"
    database_mock.tournament.create.assert_called_with(tournament=Tournament(
        id="Test tournament",
        creation=mock.ANY,
        players={},
        rounds=[]
    ))


def test_get_current_select_and_list_tournaments(temporary_data_root, unselect_current_tournament):
    assert get_current() is None

    create(tournament_id="a")
    create(tournament_id="b")

    assert get_current() == "b"
    select("a")
    assert get_current() == "a"

    assert list_tournaments() == ["a", "b"]


@mock.patch('dune_tournament_scoreboard.controllers.tournament.database')
def test_create_update_get_list_and_deactivate_player(database_mock, reset_current_tournament):
    assert get_player('test') is None

    player_id = create_player(name="Hello", surname="World")
    expected_player = Player(id=player_id, name="Hello", surname="World", is_active=True)
    assert get_player(player_id) == expected_player
    database_mock.player.save.assert_called_with(mock.ANY, player=expected_player)

    expected_player.surname = "World!"
    update_player(expected_player)
    deactivate_player(player_id)

    expected_player.is_active = False
    assert get_player(player_id) == expected_player
    database_mock.player.save.assert_called_with(mock.ANY, player=expected_player)

    assert expected_player in list_players()


@mock.patch('dune_tournament_scoreboard.controllers.tournament.database')
def test_update_get_list_scores(database_mock, reset_current_tournament):
    assert get_score('d', round_=1) == Score(4, 8, 1, 6, 8, 2)

    update_score('d', Score(3, 8, 1, 6, 8, 2), round_=-2)

    assert get_score('d', round_=1) == Score(3, 8, 1, 6, 8, 2)
    database_mock.score.save.assert_called_with(mock.ANY, round_=1, player_id='d', score=Score(3, 8, 1, 6, 8, 2))
