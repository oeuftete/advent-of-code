from collections import defaultdict

import attr
from aocd.models import Puzzle  # type: ignore


@attr.s
class OctopusGrid:
    raw_lines: list[str] = attr.ib()
    grid: dict[int, dict[int, int]] = attr.ib(init=False, factory=dict)
    n_flashes: int = attr.ib(init=False, default=0)
    grid_size: int = attr.ib(init=False, default=0)
    current_step: int = attr.ib(init=False, default=0)

    def __attrs_post_init__(self) -> None:
        grid: defaultdict[int, defaultdict[int, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        for y, raw_line in enumerate(self.raw_lines):
            for x, c in enumerate(raw_line):
                grid[x][y] = int(c)
                self.grid_size += 1

        #  De-defaultdict after building
        for k in grid:
            self.grid[k] = dict(grid[k])

    def excite_neighbours(self, x, y):
        for x_n in [x - 1, x, x + 1]:
            for y_n in [y - 1, y, y + 1]:
                if x_n == x and y_n == y:
                    continue

                if self.grid.get(x_n, {}).get(y_n, 0) > 0:
                    self.grid[x_n][y_n] += 1

    def cycle_until_all_flash(self) -> None:
        while self.cycle() != self.grid_size:
            continue

    def cycle(self, iterations: int = 1) -> int:
        n_flashes_this_cycle = 0
        for _ in range(iterations):
            self.current_step += 1

            for x in self.grid.keys():
                for y in self.grid[x].keys():
                    self.grid[x][y] += 1

            for _ in range(100):  # brute force; TODO: hash for diffs
                for x in self.grid.keys():
                    for y in self.grid[x].keys():
                        if self.grid[x][y] > 9:
                            self.n_flashes += 1
                            n_flashes_this_cycle += 1
                            self.grid[x][y] = 0
                            self.excite_neighbours(x, y)

        return n_flashes_this_cycle


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=11)
    lines = puzzle.input_data.strip().splitlines()

    og = OctopusGrid(lines)
    og.cycle(100)
    puzzle.answer_a = og.n_flashes

    og = OctopusGrid(lines)
    og.cycle_until_all_flash()
    puzzle.answer_b = og.current_step
