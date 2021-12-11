from collections import defaultdict

import attr
from aocd.models import Puzzle  # type: ignore
from cached_property import cached_property  # type: ignore


@attr.s
class HeightMap:
    raw_lines: list[str] = attr.ib()
    grid: dict[int, dict[int, int]] = attr.ib(init=False, factory=dict)
    low_points: list[tuple[int, int, int]] = attr.ib(init=False, factory=list)

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

    def all_neighbours_lower(self, x, y, v) -> bool:
        for t in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if self.grid.get(t[0], {}).get(t[1], 10) <= v:
                return False

        return True

    @cached_property
    def risk_level_sum(self) -> int:
        return sum(map(lambda t: t[2] + 1, self.low_points))


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=9)
    lines = puzzle.input_data.strip().splitlines()

    hm = HeightMap(lines)
    puzzle.answer_a = hm.risk_level_sum
