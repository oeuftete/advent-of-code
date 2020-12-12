import itertools
import logging
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class SeatingArea:
    raw_grid: str
    grid: dict = field(init=False, default_factory=dict)
    width: int = field(init=False)
    height: int = field(init=False)

    def __repr__(self):
        grid_str = ""
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                grid_str += self.grid[x][y]
            grid_str += "\n"

        return grid_str.strip()

    def __post_init__(self):
        for y, row in enumerate(self.raw_grid.splitlines()):
            for x, c in enumerate(row):
                try:
                    self.grid[x][y] = c
                except KeyError:
                    self.grid[x] = {}
                    self.grid[x][y] = c

        self.width = x  # pylint: disable=undefined-loop-variable
        self.height = y  # pylint: disable=undefined-loop-variable

    def reseat(self, n=1):
        starting_grid = deepcopy(self.grid)
        for i in itertools.count(1):
            if i > n:
                break
            for y in range(self.height + 1):
                for x in range(self.width + 1):
                    c = starting_grid[x][y]
                    if c == ".":
                        continue

                    surroundings = Counter()
                    for d in [
                        (-1, -1),
                        (-1, 0),
                        (-1, 1),
                        (0, -1),
                        (0, 1),
                        (1, -1),
                        (1, 0),
                        (1, 1),
                    ]:
                        #  logging.debug("(%s, %s) looking at %s...", x, y, d)
                        try:
                            neighbour = starting_grid[x + d[0]][y + d[1]]
                            #  logging.debug(
                            #      "...(%s, %s) found neighbour (%s)", x, y, neighbour
                            #  )
                            surroundings[neighbour] += 1
                        except KeyError:
                            #  logging.debug("...(%s, %s) no neighbour", x, y)
                            surroundings["."] += 1

                    #  logging.debug("(%s, %s) Counter = %s", x, y, surroundings)

                    if c == "L" and surroundings["#"] == 0:
                        self.grid[x][y] = "#"
                    elif c == "#" and surroundings["#"] >= 4:
                        self.grid[x][y] = "L"

        logging.debug(self)

    def reseat_until_stable(self, max_iterations=1_000_000):
        previous_grid = {}
        for i in itertools.count():
            if i > max_iterations or self.grid == previous_grid:
                break
            previous_grid = deepcopy(self.grid)
            self.reseat()

    @property
    def occupied_seats(self):
        occupied = Counter()
        for x in self.grid:
            for y in self.grid[x]:
                occupied[self.grid[x][y]] += 1
        return occupied["#"]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=11)
    seating_area = SeatingArea(puzzle.input_data)
    seating_area.reseat_until_stable()
    puzzle.answer_a = seating_area.occupied_seats
