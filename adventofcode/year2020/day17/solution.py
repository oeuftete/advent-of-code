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
    w: int = 0
    is_hypercube: bool = False

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.w, self.is_hypercube))

    @property
    def neighbours(self):
        neighbours = []
        for ox in range(self.x - 1, self.x + 2):
            for oy in range(self.y - 1, self.y + 2):
                for oz in range(self.z - 1, self.z + 2):
                    wrange = range(self.w - 1, self.w + 2) if self.is_hypercube else [0]
                    for ow in wrange:
                        if (
                            ox == self.x
                            and oy == self.y
                            and oz == self.z
                            and ow == self.w
                        ):
                            continue
                        neighbours.append((ox, oy, oz, ow))
        return neighbours


@dataclass
class CubeEngine:
    initial_grid: str
    grid: dict = field(default_factory=lambda: defaultdict(lambda: "."))
    is_hypercube: bool = False

    def __repr__(self):
        r = ""
        b = self.boundaries()
        wrange = range(b["w"][0], b["w"][1] + 1) if self.is_hypercube else [0]
        for w in wrange:
            for z in range(b["z"][0], b["z"][1] + 1):
                r += f"z={z} w={w}\n"
                for y in range(b["y"][0], b["y"][1] + 1):
                    for x in range(b["x"][0], b["x"][1] + 1):
                        r += self.grid[CubeCell(x, y, z, w, self.is_hypercube)]
                    r += "\n"
                r += "\n"

        return r

    def __post_init__(self):
        # parse initial_grid, x increases rightward, y downward
        z = w = 0
        for y, line in enumerate(self.initial_grid.strip().splitlines()):
            for x, state in enumerate(line):
                self.grid[CubeCell(x, y, z, w, self.is_hypercube)] = state

    @property
    def active_cells(self) -> int:
        return len([state for state in self.grid.values() if state == "#"])

    def boundaries(self):
        min_x = min_y = min_z = min_w = math.inf
        max_x = max_y = max_z = max_w = -math.inf

        for cc in self.grid.keys():
            max_x = cc.x if cc.x > max_x else max_x
            max_y = cc.y if cc.y > max_y else max_y
            max_z = cc.z if cc.z > max_z else max_z
            max_w = cc.w if cc.w > max_w else max_w
            min_x = cc.x if cc.x < min_x else min_x
            min_y = cc.y if cc.y < min_y else min_y
            min_z = cc.z if cc.z < min_z else min_z
            min_w = cc.w if cc.w < min_w else min_w
        return {
            "x": (min_x, max_x),
            "y": (min_y, max_y),
            "z": (min_z, max_z),
            "w": (min_w, max_w),
        }

    def iterate(self, n=1):
        # pylint: disable=too-many-nested-blocks
        for _ in range(n):
            new_grid = deepcopy(self.grid)
            logging.debug(
                {cc: state for (cc, state) in self.grid.items() if state == "#"}
            )
            b = self.boundaries()
            for x in range(b["x"][0] - 1, b["x"][1] + 2):
                for y in range(b["y"][0] - 1, b["y"][1] + 2):
                    for z in range(b["z"][0] - 1, b["z"][1] + 2):
                        wrange = (
                            range(b["w"][0] - 1, b["w"][1] + 2)
                            if self.is_hypercube
                            else [0]
                        )
                        for w in wrange:
                            cc = CubeCell(x, y, z, w, self.is_hypercube)
                            state = self.grid[cc]
                            grid_neighbours = [
                                self.grid[CubeCell(*xyzw, self.is_hypercube)]
                                for xyzw in cc.neighbours
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

            self.grid = new_grid
            logging.debug(self)


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=17)
    initial_grid = puzzle.input_data.strip()
    cube_engine = CubeEngine(initial_grid)
    cube_engine.iterate(6)

    puzzle.answer_a = cube_engine.active_cells

    cube_engine = CubeEngine(initial_grid, is_hypercube=True)
    cube_engine.iterate(6)

    puzzle.answer_b = cube_engine.active_cells
