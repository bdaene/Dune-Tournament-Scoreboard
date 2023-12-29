from typing import TypeAlias
from uuid import uuid4

from attr import define, field

PlayerId: TypeAlias = str


@define
class Player:
    name: str
    surname: str
    id: PlayerId = field(factory=lambda: uuid4().hex)
    is_active: bool = field(default=True, converter=bool)

    @property
    def full_name(self):
        return f"{self.name.capitalize()} {self.surname.title()}"
