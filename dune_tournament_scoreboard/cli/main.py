from pathlib import Path

import click
import yaml

from dune_tournament_scoreboard import controllers
from dune_tournament_scoreboard.cli.player import player_group
from dune_tournament_scoreboard.cli.round import round_group
from dune_tournament_scoreboard.cli.tournament import tournament_group


@click.group()
@click.option('-c', '--config', 'config_path', default='./config.yml', type=Path)
@click.version_option()
@click.pass_context
def scoreboard(context, config_path):
    context.config = load_or_create_config(config_path)

    current_tournament = context.config.get('current_tournament')
    if current_tournament is not None:
        controllers.tournament.select(current_tournament)


scoreboard.add_command(tournament_group)
scoreboard.add_command(player_group)
scoreboard.add_command(round_group)


def load_or_create_config(config_path: Path) -> dict:
    if config_path.exists():
        with open(config_path) as config_file:
            return yaml.safe_load(config_file)

    config = dict(
        current_tournament=controllers.tournament.get_current()
    )
    with open(config_path, 'w') as config_file:
        yaml.safe_dump(config, config_file)
    return config


if __name__ == "__main__":
    scoreboard()
