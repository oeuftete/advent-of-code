import logging
from collections import defaultdict
from functools import cached_property, reduce
from operator import mul

import attr
from aocd.models import Puzzle  # type: ignore

LOGGER = logging.getLogger("solveaocd")


@attr.s
class Basin:
    low_point: tuple[int, int] = attr.ib()
    points: set[tuple[int, int]] = attr.ib(init=False, factory=set)


@attr.s
class HeightMap:
    raw_lines: list[str] = attr.ib()
    grid: dict[int, dict[int, int]] = attr.ib(init=False, factory=dict)
    low_points: list[tuple[int, int, int]] = attr.ib(init=False, factory=list)
    basins: list[Basin] = attr.ib(init=False, factory=list)
    memoized_low_points: dict[tuple[int, int], tuple[int, int]] = attr.ib(
        init=False, factory=dict
    )

    def __attrs_post_init__(self) -> None:
        grid: defaultdict[int, defaultdict[int, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        for y, raw_line in enumerate(self.raw_lines):
            for x, c in enumerate(raw_line):
                grid[x][y] = int(c)

        #  De-defaultdict after building
        for k in grid:
            self.grid[k] = dict(grid[k])

        #  Calculate the low points
        for x in self.grid.keys():
            for y in self.grid[x].keys():
                if self.all_neighbours_lower(x, y, self.grid[x][y]):
                    self.low_points.append((x, y, self.grid[x][y]))
                    self.basins.append(Basin((x, y)))

        #  Assign points to basins
        for x in self.grid.keys():
            for y in self.grid[x].keys():
                LOGGER.debug(
                    "Looking for lowest point for [%d,%d] = %d", x, y, self.grid[x][y]
                )
                lx, ly = self.get_lowest_point_for(x, y)
                LOGGER.debug(
                    "... found lowest point for [%d,%d] = %d -> (%d, %d)",
                    x,
                    y,
                    self.grid[x][y],
                    lx,
                    ly,
                )
                if self.is_basin_at(lx, ly):
                    LOGGER.debug(
                        "Adding lowest point for [%d,%d] to basin at (%d,%d)",
                        x,
                        y,
                        lx,
                        ly,
                    )
                    self.get_basin_at(lx, ly).points.add((x, y))

    def get_basin_at(self, x, y) -> Basin:
        return next(filter(lambda b: b.low_point == (x, y), self.basins))

    def is_basin_at(self, x, y) -> bool:
        try:
            self.get_basin_at(x, y)
            return True
        except StopIteration:
            return False

    def get_lowest_point_for(self, x, y) -> tuple[int, int]:
        if self.grid[x][y] == 9:
            return (-1, -1)

        if self.is_basin_at(x, y):
            return (x, y)

        saved_low_point = None
        for t in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if self.is_basin_at(t[0], t[1]):
                LOGGER.debug("Memoizing result for [%d,%d]: %s", x, y, t)
                self.memoized_low_points[(x, y)] = t
                return t

            if self.grid.get(t[0], {}).get(t[1], 10) < self.grid[x][y]:
                saved_low_point = t

        try:
            t = self.memoized_low_points[saved_low_point]
            LOGGER.debug("Returning memoized result for [%d,%d]: %s", x, y, t)
            return t
        except KeyError:
            pass

        LOGGER.debug(
            "Recursing for [%d,%d] at next low point: %s", x, y, saved_low_point
        )
        return self.get_lowest_point_for(*saved_low_point)

    def all_neighbours_lower(self, x, y, v) -> bool:
        for t in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if self.grid.get(t[0], {}).get(t[1], 10) <= v:
                return False

        return True

    @cached_property
    def risk_level_sum(self) -> int:
        return sum(map(lambda t: t[2] + 1, self.low_points))

    @cached_property
    def basin_product(self) -> int:
        return reduce(
            mul, list(reversed(sorted(map(lambda b: len(b.points), self.basins))))[:3]
        )


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=9)
    lines = puzzle.input_data.strip().splitlines()

    hm = HeightMap(lines)
    puzzle.answer_a = hm.risk_level_sum
    puzzle.answer_b = hm.basin_product
