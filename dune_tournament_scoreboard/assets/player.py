from typing import TypeAlias
from uuid import uuid4

from attrs import define, field

PlayerId: TypeAlias = str


@define
class Player:
    name: str = field(converter=str.upper)
    surname: str = field(converter=str.title)
    id: PlayerId = field(factory=lambda: uuid4().hex)
    is_active: bool = field(default=True, converter=bool)
