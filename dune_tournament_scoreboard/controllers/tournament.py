from dune_tournament_scoreboard import services
from dune_tournament_scoreboard.assets.tournament import Tournament

known_tournaments: set[str] = list_tournaments
current_tournament: Tournament = load_last_or_create()


def load_last_or_create():
    tournament = services.database.tournament.load_last()