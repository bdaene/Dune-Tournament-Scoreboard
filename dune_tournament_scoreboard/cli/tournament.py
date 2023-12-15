import click

from dune_tournament_scoreboard import controllers


@click.group('tournament')
def tournament_group():
    pass


@tournament_group.command()
@click.argument('id_')
def create(id_):
    controllers.tournament.create(id_=id_)


@tournament_group.command()
@click.argument('id_')
def select(id_):
    controllers.tournament.select(id_=id_)


@tournament_group.command('list')
def list_all():
    controllers.tournament.list_tournaments()
