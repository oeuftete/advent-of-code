import typing
from collections import defaultdict

import attr
from aocd.models import Puzzle  # type: ignore

from adventofcode.common.coordinate import Coordinate


@attr.s
class VentMap:
    lines: typing.List[str] = attr.ib()
    grid: typing.Dict[Coordinate, int] = attr.ib(init=False, default=defaultdict(int))

    def __attrs_post_init__(self):
        for line in self.lines:
            line_start, line_end = map(
                lambda c: Coordinate(*tuple(map(int, c.split(",")))), line.split(" -> ")
            )

            if line_start.x == line_end.x:
                y_endpoints = sorted((line_start.y, line_end.y))
                for y in range(y_endpoints[0], y_endpoints[1] + 1):
                    self.grid[Coordinate(line_start.x, y)] += 1

            if line_start.y == line_end.y:
                x_endpoints = sorted((line_start.x, line_end.x))
                for x in range(x_endpoints[0], x_endpoints[1] + 1):
                    self.grid[Coordinate(x, line_start.y)] += 1

    @property
    def danger_spots(self) -> typing.List[Coordinate]:
        danger_spots = []
        for c, line_count in self.grid.items():
            if line_count > 1:
                danger_spots.append(c)

        return danger_spots


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=5)
    lines = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = len(VentMap(lines).danger_spots)
