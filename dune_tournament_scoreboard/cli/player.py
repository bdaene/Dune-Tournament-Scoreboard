from typing import Optional

import click
from attrs import asdict

from dune_tournament_scoreboard import controllers
from dune_tournament_scoreboard.assets.player import Player


def _format_player(player: Optional[Player]) -> str:
    if player is None:
        data = dict(id="ID", name='NAME', surname='Surname', is_active='is active?')
    else:
        data = asdict(player)
    return "{id: <32} {name: <32} {surname: <32} {is_active!s: <20}".format(**data)


@click.group('player')
def player_group():
    pass


@player_group.command(help="Create a new player.")
@click.argument('name')
@click.argument('surname')
def create(name, surname):
    controllers.tournament.create_player(name=name, surname=surname)


@player_group.command(help="Get player info for the given ID.")
@click.argument('player_id')
def get(player_id):
    click.echo(_format_player(controllers.tournament.get_player(player_id)))


@player_group.command('list', help="List all players.")
def list_all():
    click.echo(_format_player(None))
    for player in controllers.tournament.list_players():
        click.echo(_format_player(player))


@player_group.command(help="Update the player info for the given ID.")
@click.argument('player_id')
@click.argument('name')
@click.argument('surname')
def update(player_id, name, surname):
    controllers.tournament.update_player(Player(id=player_id, name=name, surname=surname))


@player_group.command(help="Deactivate the player with the given ID.")
@click.argument('player_id')
def deactivate(player_id):
    controllers.tournament.deactivate_player(player_id)
