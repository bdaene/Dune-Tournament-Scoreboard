from typing import Optional

import attrs
import click

from dune_tournament_scoreboard import controllers
from dune_tournament_scoreboard.assets.player import Player
from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.assets.tournament import TournamentId


@click.group('tournament')
def tournament_group():
    pass


@tournament_group.command(help="Create a new tournament.")
@click.argument('tournament_id')
def create(tournament_id: TournamentId):
    controllers.tournament.create(tournament_id=tournament_id)


@tournament_group.command(help="Select the tournament with the given ID.")
@click.argument('tournament_id')
def select(tournament_id: TournamentId):
    controllers.tournament.select(tournament_id=tournament_id)


@tournament_group.command('current', help="Get the ID of the currently selected tournament.")
def get_current():
    click.echo(controllers.tournament.get_current())


@tournament_group.command('list', help="List all existing tournaments.")
def list_all():
    for tournament in controllers.tournament.list_tournaments():
        click.echo(tournament)


def _format_entry(entry: Optional[tuple[Player, list[int], Score]], rounds: int) -> str:
    if entry is None:
        data = dict(
            name='NAME',
            surname='Surname',
        )
        data |= {f"round_{i}": f"Round {i}" for i in range(rounds)}
        data |= dict(
            tournament_points='Tournament points',
            victory_points='Victory points',
            spice='Spice',
            solaris='Solaris',
            water='Water',
            troops_in_garrison='Troops in Garrison'
        )
    else:
        player, tournament_points, score = entry
        data = dict(
            name=player.name,
            surname=player.surname,
        )
        data |= {f"round_{i}": round_ for i, round_ in enumerate(tournament_points)}
        data |= attrs.asdict(score)

    entry_format = ["{name: <32}", "{surname: <32}"]
    entry_format += [f"{{round_{i}: <8}}" for i in range(rounds)]
    entry_format += ["{tournament_points: <18}", "{victory_points: <18}", "{spice: <18}", "{solaris: <18}",
                     "{water: <18}", "{troops_in_garrison: <18}"]
    return " ".join(entry_format).format(**data)


@tournament_group.command('summary', help="Show the summary board of the current tournament.")
def get_summary():
    summary = controllers.tournament.get_summary()
    rounds = max(len(entry[1]) for entry in summary)
    click.echo(_format_entry(None, rounds))
    for entry in summary:
        click.echo(_format_entry(entry, rounds))
