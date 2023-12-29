import atexit
from pathlib import Path

import click
import yaml

from dune_tournament_scoreboard import controllers
from dune_tournament_scoreboard.cli.player import player_group
from dune_tournament_scoreboard.cli.round import round_group
from dune_tournament_scoreboard.cli.tournament import tournament_group


@click.group(invoke_without_command=True)
@click.option('-c', '--config', 'config_path', default='./config.yml', type=Path)
@click.version_option()
def scoreboard(config_path):
    load_config(config_path)
    atexit.register(lambda: save_config(config_path))


scoreboard.add_command(tournament_group)
scoreboard.add_command(player_group)
scoreboard.add_command(round_group)


def load_config(config_path: Path):
    if config_path.exists():
        with open(config_path) as config_file:
            config = yaml.safe_load(config_file)

        current_tournament = config.get('current_tournament')
        if current_tournament:
            try:
                controllers.tournament.select(current_tournament)
            except ValueError:
                pass


def save_config(config_path: Path):
    config = dict(
        current_tournament=controllers.tournament.get_current()
    )
    with open(config_path, 'w') as config_file:
        yaml.safe_dump(config, config_file)


if __name__ == "__main__":
    scoreboard()
