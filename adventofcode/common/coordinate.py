from __future__ import annotations

import attr


@attr.s(frozen=True)
class Coordinate:
    x: int = attr.ib(default=0)
    y: int = attr.ib(default=0)

    @classmethod
    def from_csv(cls, csv: str) -> Coordinate:
        return cls(*(map(int, csv.replace(" ", "").split(","))))

    def manhattan_distance(self, other: Coordinate) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def is_bounded_by(self, other: Coordinate, direction: str):
        if direction == "east":
            return self.x < other.x and (other.x - self.x) >= abs(self.y - other.y)
        if direction == "west":
            return self.x > other.x and (self.x - other.x) >= abs(self.y - other.y)
        if direction == "north":
            return self.y < other.y and (other.y - self.y) >= abs(self.x - other.x)
        if direction == "south":
            return self.y > other.y and (self.y - other.y) >= abs(self.x - other.x)

        raise ValueError
