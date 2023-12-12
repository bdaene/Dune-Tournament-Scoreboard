from dataclasses import dataclass
from typing import TypeAlias

PlayerId: TypeAlias = str


@dataclass
class Player:
    id: PlayerId
    name: str
    surname: str

