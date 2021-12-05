import logging
import typing
from collections import defaultdict

import attr
from aocd.models import Puzzle  # type: ignore

from adventofcode.common.coordinate import Coordinate

logging.basicConfig(level=logging.INFO)


@attr.s
class VentMap:
    lines: typing.List[str] = attr.ib()
    grid: typing.Dict[Coordinate, int] = attr.ib(
        init=False, factory=lambda: defaultdict(int)
    )
    check_diagonals: bool = attr.ib(default=False)

    def __attrs_post_init__(self):
        for line in self.lines:
            line_start, line_end = sorted(
                map(
                    lambda c: Coordinate(*tuple(map(int, c.split(",")))),
                    line.split(" -> "),
                )
            )

            if line_start.x == line_end.x:
                y_endpoints = sorted((line_start.y, line_end.y))
                for y in range(y_endpoints[0], y_endpoints[1] + 1):
                    logging.debug(
                        "Marking a horizontal line at [%d, %d]", line_start.x, y
                    )
                    self.grid[Coordinate(line_start.x, y)] += 1
                    logging.debug(
                        "... new value = %d", self.grid[Coordinate(line_start.x, y)]
                    )

            elif line_start.y == line_end.y:
                for x in range(line_start.x, line_end.x + 1):  # x already sorted
                    logging.debug(
                        "Marking a vertical line at [%d, %d]", x, line_start.y
                    )
                    self.grid[Coordinate(x, line_start.y)] += 1
                    logging.debug(
                        "... new value = %d", self.grid[Coordinate(x, line_start.y)]
                    )

            elif self.check_diagonals:
                y_step = 1 if line_start.y < line_end.y else -1
                y = line_start.y
                for x in range(line_start.x, line_end.x + 1):  # x already sorted
                    logging.debug("Marking a diagonal line at [%d, %d]...", x, y)
                    self.grid[Coordinate(x, y)] += 1
                    logging.debug("... new value = %d", self.grid[Coordinate(x, y)])
                    y += y_step

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
    puzzle.answer_b = len(VentMap(lines, check_diagonals=True).danger_spots)
