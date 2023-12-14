from datetime import timezone, datetime

from dune_tournament_scoreboard import services
from dune_tournament_scoreboard.assets.tournament import Tournament, TournamentId


def create(id_: TournamentId) -> Tournament:
    tournament = Tournament(
        id=id_,
        creation=datetime.now(tz=timezone.utc),
        players={},
        rounds=[]
    )

    services.database.tournament.create(tournament)

    return tournament


def save(tournament: Tournament):
    cursor = services.database.tournament.get_cursor()
    services.database.tournament.save(cursor, tournament)
    services.database.tournament.commit()


def load(tournament_id):
    services.database.tournament.select(tournament_id)
    cursor = services.database.tournament.get_cursor()
    return services.database.tournament.load(cursor)
