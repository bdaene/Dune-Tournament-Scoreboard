from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias

from dune_tournament_scoreboard.assets.board import Board

TournamentId: TypeAlias = str


@dataclass
class Tournament:
    id: TournamentId
    board: Board
    creation: datetime
