import random

from dune_tournament_scoreboard import controllers
from tests.assets._test_board import _get_test_board


def main():
    tournament_id = f"tournament_{random.randrange(1_000_000)}"

    tournament = controllers.tournament.create(id=tournament_id)
    tournament.board = _get_test_board()
    controllers.tournament.save(tournament)

    tournament = controllers.tournament.load(tournament_id)

    print(tournament)


if __name__ == "__main__":
    main()
