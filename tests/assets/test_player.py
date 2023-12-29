from dune_tournament_scoreboard.assets.player import Player


def test_full_name():
    assert Player(name="hello", surname="world").full_name == "HELLO World"
