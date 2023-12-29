from datetime import datetime, timezone
from typing import TypeAlias

from attr import define, field

from dune_tournament_scoreboard.assets.player import PlayerId, Player
from dune_tournament_scoreboard.assets.round import Round

TournamentId: TypeAlias = str


@define
class Tournament:
    id: TournamentId
    creation: datetime = field(factory=lambda: datetime.now(tz=timezone.utc))
    players: dict[PlayerId: Player] = field(factory=dict)
    rounds: list[Round] = field(factory=list)
