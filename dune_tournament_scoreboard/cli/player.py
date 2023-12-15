import click

from dune_tournament_scoreboard import controllers


@click.group('player')
def player_group():
    pass


@player_group.command()
@click.argument('name')
@click.argument('surname')
def create(name, surname):
    controllers.tournament.create_player(name=name, surname=surname)


@player_group.command('list')
def list_all():
    line_format = "{id: >32} {name: >32} {surname: >32}"

    click.echo(line_format.format(id='ID', name='NAME', surname='Surname'))
    for player in controllers.tournament.list_players():
        click.echo(line_format.format(id=player.id, name=player.name, surname=player.surname))
