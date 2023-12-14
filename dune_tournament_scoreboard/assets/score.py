from __future__ import annotations

from attr import define


@define(order=True)
class Score:
    tournament_points: int = 0
    victory_points: int = 0
    spice: int = 0
    solaris: int = 0
    water: int = 0
    troops_in_garrison: int = 0

    def __add__(self, other: Score) -> Score:
        return Score(
            tournament_points=self.tournament_points + other.tournament_points,
            victory_points=self.victory_points + other.victory_points,
            spice=self.spice + other.spice,
            solaris=self.solaris + other.solaris,
            water=self.water + other.water,
            troops_in_garrison=self.troops_in_garrison + other.troops_in_garrison,
        )
