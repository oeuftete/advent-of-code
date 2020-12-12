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
        grid_rows = []
        for x in range(self.width):
            row_str = ""
            for y in range(self.height):
                try:
                    row_str += self.grid[y][x]
                except KeyError:
                    row_str += "?"
            grid_rows.append(row_str)

        return "\n".join(grid_rows)

    def __post_init__(self):
        for y, row in enumerate(self.raw_grid.splitlines()):
            for x, c in enumerate(row.strip()):
                try:
                    self.grid[x][y] = c
                except KeyError:
                    self.grid[x] = {}
                    self.grid[x][y] = c
        self.width = x + 1  # pylint: disable=undefined-loop-variable
        self.height = y + 1  # pylint: disable=undefined-loop-variable

    @classmethod
    def nearest_counter(cls, x, y, starting_grid, algorithm="original"):
        surroundings = Counter()
        spaces_to_check = ["L", "#"]
        if algorithm == "original":
            spaces_to_check.append(".")

        for ix in itertools.count(start=x + 1):
            try:
                c = starting_grid[ix][y]
                if c in spaces_to_check:
                    surroundings[c] += 1
                    break
            except KeyError:
                break

        for ix in itertools.count(start=x - 1, step=-1):
            try:
                c = starting_grid[ix][y]
                if c in spaces_to_check:
                    surroundings[c] += 1
                    break
            except KeyError:
                break

        for iy in itertools.count(start=y + 1):
            try:
                c = starting_grid[x][iy]
                if c in spaces_to_check:
                    surroundings[c] += 1
                    break
            except KeyError:
                break

        for iy in itertools.count(start=y - 1, step=-1):
            try:
                c = starting_grid[x][iy]
                if c in spaces_to_check:
                    surroundings[c] += 1
                    break
            except KeyError:
                break

        for dy, ix in enumerate(itertools.count(start=x + 1), start=1):
            try:
                c = starting_grid[ix][y + dy]
                if c in spaces_to_check:
                    surroundings[c] += 1
                    break
            except KeyError:
                break

        for dy, ix in enumerate(itertools.count(start=x + 1), start=1):
            try:
                c = starting_grid[ix][y - dy]
                if c in spaces_to_check:
                    surroundings[c] += 1
                    break
            except KeyError:
                break

        for dy, ix in enumerate(itertools.count(start=x - 1, step=-1), start=1):
            try:
                c = starting_grid[ix][y + dy]
                if c in spaces_to_check:
                    surroundings[c] += 1
                    break
            except KeyError:
                break

        for dy, ix in enumerate(itertools.count(start=x - 1, step=-1), start=1):
            try:
                c = starting_grid[ix][y - dy]
                if c in spaces_to_check:
                    surroundings[c] += 1
                    break
            except KeyError:
                break

        return surroundings

    def reseat(self, n=1, algorithm="original"):
        starting_grid = deepcopy(self.grid)
        for i in itertools.count(1):
            if i > n:
                break
            for x in range(self.width):
                for y in range(self.height):
                    c = starting_grid[x][y]
                    if c == ".":
                        continue

                    surroundings = self.nearest_counter(x, y, starting_grid, algorithm)

                    #  logging.debug("(%s, %s) Counter = %s", x, y, surroundings)

                    leave_threshold = 4 if algorithm == "original" else 5
                    if c == "L" and surroundings["#"] == 0:
                        self.grid[x][y] = "#"
                    elif c == "#" and surroundings["#"] >= leave_threshold:
                        self.grid[x][y] = "L"

        logging.debug(self)

    def reseat_until_stable(self, max_iterations=1_000_000, algorithm="original"):
        previous_grid = {}
        for i in itertools.count():
            if i > max_iterations or self.grid == previous_grid:
                break
            previous_grid = deepcopy(self.grid)
            self.reseat(algorithm=algorithm)

    @property
    def occupied_seats(self):
        occupied = Counter()
        for x in range(self.width):
            for y in range(self.height):
                occupied[self.grid[x][y]] += 1
        return occupied["#"]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=11)
    seating_area = SeatingArea(puzzle.input_data)
    seating_area.reseat_until_stable()
    puzzle.answer_a = seating_area.occupied_seats

    seating_area = SeatingArea(puzzle.input_data)
    seating_area.reseat_until_stable(algorithm="alt")
    puzzle.answer_b = seating_area.occupied_seats
