import logging
import math
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class CubeCell:
    x: int = 0
    y: int = 0
    z: int = 0

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    @property
    def neighbours(self):
        neighbours = []
        for ox in range(self.x - 1, self.x + 2):
            for oy in range(self.y - 1, self.y + 2):
                for oz in range(self.z - 1, self.z + 2):
                    if ox == self.x and oy == self.y and oz == self.z:
                        continue
                    neighbours.append((ox, oy, oz))
        return neighbours


@dataclass
class CubeEngine:
    initial_grid: str
    grid: dict = field(default_factory=lambda: defaultdict(lambda: "."))

    def __repr__(self):
        b = self.boundaries()
        for z in range(b["z"][0], b["z"][1] + 1):
            print(f"z={z}\n")
            for y in range(b["y"][0], b["y"][1] + 1):
                for x in range(b["x"][0], b["x"][1] + 1):
                    print(self.grid[CubeCell(x, y, z)])
                print("\n")
            print("\n")

    @property
    def _stripped_grid(self):
        return {cc: state for (cc, state) in self.grid.items() if state == "#"}

    def __post_init__(self):
        # parse initial_grid, x increases rightward, y downward
        z = 0
        for y, line in enumerate(self.initial_grid.strip().splitlines()):
            for x, state in enumerate(line):
                self.grid[CubeCell(x, y, z)] = state

    @property
    def active_cells(self) -> int:
        #  self._strip_inactive()
        #  return len(self.grid)
        return len([state for state in self.grid.values() if state == "#"])

    def boundaries(self):
        min_x = min_y = min_z = math.inf
        max_x = max_y = max_z = -math.inf

        for cc in self.grid.keys():
            max_x = cc.x if cc.x > max_x else max_x
            max_y = cc.y if cc.y > max_y else max_y
            max_z = cc.z if cc.z > max_z else max_z
            min_x = cc.x if cc.x < min_x else min_x
            min_y = cc.y if cc.y < min_y else min_y
            min_z = cc.z if cc.z < min_z else min_z
        return {
            "x": (min_x, max_x),
            "y": (min_x, max_x),
            "z": (min_x, max_x),
        }

    def iterate(self, n=1):
        #  self._strip_inactive()
        for _ in range(n):
            new_grid = deepcopy(self.grid)
            logging.debug(
                {cc: state for (cc, state) in self.grid.items() if state == "#"}
            )
            b = self.boundaries()
            for x in range(b["x"][0] - 1, b["x"][1] + 2):
                for y in range(b["y"][0] - 1, b["y"][1] + 2):
                    for z in range(b["z"][0] - 1, b["z"][1] + 2):
                        cc = CubeCell(x, y, z)
                        state = self.grid[cc]
                        grid_neighbours = [
                            self.grid[CubeCell(*xyz)] for xyz in cc.neighbours
                        ]
                        n_active_neighbours = len(
                            [gn for gn in grid_neighbours if gn == "#"]
                        )

                        logging.debug(
                            "Active neighbours for %s (%s): %s",
                            cc,
                            state,
                            n_active_neighbours,
                        )

                        if state == "#" and n_active_neighbours not in (2, 3):
                            logging.debug("Setting %s to [.]", cc)
                            new_grid[cc] = "."
                        elif state == "." and n_active_neighbours == 3:
                            logging.debug("Setting %s to [#]", cc)
                            new_grid[cc] = "#"
                        else:
                            new_grid[cc] = state

            logging.debug(new_grid)
            self.grid = new_grid


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=17)
    initial_grid = puzzle.input_data.strip()
    cube_engine = CubeEngine(initial_grid)
    cube_engine.iterate(6)

    puzzle.answer_a = cube_engine.active_cells
