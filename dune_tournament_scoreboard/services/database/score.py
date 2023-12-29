import sqlite3

from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.assets.player import PlayerId


def create_table(cursor: sqlite3.Cursor):
    cursor.execute("""CREATE TABLE score(
    round INTEGER NOT NULL,
    player_id TEXT NOT NULL,
    tournament_points INTEGER NOT NULL,
    victory_points INTEGER NOT NULL,
    spice INTEGER NOT NULL,
    solaris INTEGER NOT NULL,
    water INTEGER NOT NULL,
    troops_in_garrison INTEGER NOT NULL,
    
    UNIQUE (round, player_id),
    
    PRIMARY KEY (round, player_id),
    FOREIGN KEY (player_id) REFERENCES player(id)
    )""")


def save_all(cursor: sqlite3.Cursor, round_: int, scores: dict[PlayerId: Score]):
    for player_id, score in scores.items():
        save(cursor, round_, player_id, score)


def save(cursor: sqlite3.Cursor, round_: int, player_id: PlayerId, score: Score):
    cursor.execute(
        """REPLACE INTO score (round, player_id, tournament_points, victory_points, spice, solaris, water,
        troops_in_garrison) VALUES (:round, :player_id, :tournament_points, :victory_points, :spice, :solaris, :water,
        :troops_in_garrison)""",
        dict(round=round_, player_id=player_id, tournament_points=score.tournament_points,
             victory_points=score.victory_points, spice=score.spice, solaris=score.solaris, water=score.water,
             troops_in_garrison=score.troops_in_garrison)
    )


def load_all(cursor: sqlite3.Cursor, round_: int) -> dict[PlayerId: Score]:
    scores = cursor.execute("""SELECT player_id, tournament_points, victory_points, spice, solaris, water,
        troops_in_garrison FROM score WHERE round = :round""", dict(round=round_)).fetchall()
    return {player_id: Score(*score) for player_id, *score in scores}
