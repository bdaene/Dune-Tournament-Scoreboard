from uuid import uuid4

from dune_tournament_scoreboard.assets.player import Player


def create(name: str, surname: str):
    return Player(id=uuid4().hex, name=name, surname=surname)
