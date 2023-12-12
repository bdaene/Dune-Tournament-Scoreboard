from dataclasses import dataclass
from datetime import datetime

from dune_tournament_scoreboard.assets.board import Board


@dataclass
class Tournament:
    id: str
    board: Board
    creation_date: datetime
