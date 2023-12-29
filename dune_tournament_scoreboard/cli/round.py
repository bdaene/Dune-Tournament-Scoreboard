from typing import Optional

import click
from attrs import asdict

from dune_tournament_scoreboard import controllers
from dune_tournament_scoreboard.assets.player import Player
from dune_tournament_scoreboard.assets.score import Score


@click.group('round')
def round_group():
    pass


@round_group.command(help="Create a new round.")
def new():
    controllers.tournament.create_new_round()
    _show_tables(round_=-1)


def _format_player(player: Optional[Player]) -> str:
    if player is None:
        data = dict(id="ID", name='NAME', surname='Surname')
    else:
        data = asdict(player)
    return "{id: <32} {name: <20} {surname: <20}".format(**data)

def _show_tables(round_: int=-1):
    click.echo(_format_player(None))
    for table in controllers.tournament.list_tables(round_=round_):
        for player in table:
            click.echo(_format_player(controllers.tournament.get_player(player)))
        click.echo()

@round_group.command(help="List the tables of a round.")
@click.option('-r', '--round', default=-1, help='Round index (default to -1).')
def tables(round):
    _show_tables(round_=round)


@round_group.command(help="Update the score of a player.")
@click.argument("player_id")
@click.argument("tournament_points")
@click.argument("victory_points")
@click.argument("spice")
@click.argument("solaris")
@click.argument("water")
@click.argument("troops_in_garrison")
@click.option('-r', '--round', default=-1, help='Round index (default to -1).')
def update(round, player_id, tournament_points, victory_points, spice, solaris, water, troops_in_garrison):
    score = Score(
        tournament_points=tournament_points,
        victory_points=victory_points,
        spice=spice,
        solaris=solaris,
        water=water,
        troops_in_garrison=troops_in_garrison,
    )
    controllers.tournament.update_score(player=player_id, score=score, round_=round)


def _format_score(score: Optional[Score]) -> str:
    if score is None:
        data = dict(
            tournament_points='TP',
            victory_points='VP',
            spice='Spice',
            solaris='Solaris',
            water='Water',
            troops_in_garrison='Troops'
        )
    else:
        data = asdict(score)

    return ("{tournament_points!s: >8} {victory_points!s: >8} {spice!s: >8} {solaris!s: >8} {water!s: >8} "
            "{troops_in_garrison!s: >8}").format(**data)


@round_group.command(help="Show the scores of a round.")
@click.option('-r', '--round', default=-1, help='Round index (default to -1).')
def scores(round):
    click.echo(f"{_format_player(None)} {_format_score(None)}")
    for table in controllers.tournament.list_tables(round_=round):
        for player in table:
            click.echo(f"{_format_player(controllers.tournament.get_player(player))} "
                       f"{_format_score(controllers.tournament.get_score(player, round))}")
        click.echo()
