import sqlite3

from dune_tournament_scoreboard.assets import Score
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
    FOREIGN KEY(player_id) REFERENCES player(id)
    )""")


def save_all(cursor: sqlite3.Cursor, scores: list[dict[PlayerId: Score]]):
    for round_, round_scores in enumerate(scores):
        for player_id, score in round_scores.items():
            save(cursor, round_, player_id, score)


def save(cursor: sqlite3.Cursor, round: int, player_id: PlayerId, score: Score):
    cursor.execute(
        """REPLACE INTO score (round, player_id, tournament_points, victory_points, spice, solaris, water,
        troops_in_garrison) VALUES (?,?,?,?,?,?,?,?)""",
        (round, player_id, score.tournament_points, score.victory_points, score.spice, score.solaris,
         score.water, score.troops_in_garrison)
    )


def load_all(cursor: sqlite3.Cursor) -> list[dict[PlayerId: Score]]:
    scores = cursor.execute("""SELECT round, player_id, tournament_points, victory_points, spice, solaris, water,
        troops_in_garrison FROM score""").fetchall()
    nb_rounds = max(round for round, *_ in scores) + 1
    rounds = [{} for _ in range(nb_rounds)]
    for round, player_id, *score in scores:
        rounds[round][player_id] = Score(*score)
    return rounds
