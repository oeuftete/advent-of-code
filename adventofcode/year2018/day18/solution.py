import logging
from collections import Counter, defaultdict

from aocd import get_data

logging.basicConfig(level=logging.INFO)

OPEN_SPACE = "."
LUMBERYARD = "#"
TREES = "|"


class Lumberyard:
    def __init__(self, string_grid):
        self._parse_grid(string_grid)

    def _parse_grid(self, s):
        self.grid = defaultdict(dict)
        y = 0
        for l in s.split("\n"):
            x = 0
            for c in l:
                if c not in [OPEN_SPACE, LUMBERYARD, TREES]:
                    raise

                self.grid[x][y] = c
                x += 1

            y += 1

    def is_open(self, x, y):
        return self.grid[x][y] == OPEN_SPACE

    def is_lumberyard(self, x, y):
        return self.grid[x][y] == LUMBERYARD

    def is_trees(self, x, y):
        return self.grid[x][y] == TREES

    @property
    def x_size(self):
        return len(self.grid.keys())

    @property
    def y_size(self):
        return len(self.grid[0].keys())

    def adjacent_points(self, x, y):
        adjacent = list()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (
                    (dx == 0 and dy == 0)
                    or (x + dx) < 0
                    or (y + dy) < 0
                    or (x + dx + 1) > self.x_size
                    or (y + dy + 1) > self.y_size
                ):
                    continue
                adjacent.append((x + dx, y + dy))

        return list(map(lambda p: self.grid[p[0]][p[1]], adjacent))

    @property
    def value(self):
        return self.grid_count[TREES] * self.grid_count[LUMBERYARD]

    @property
    def grid_count(self):
        c = Counter()
        for x in range(self.x_size):
            c.update(self.grid[x].values())

        return c

    def iterate(self, n=1):
        for i in range(n):
            new_grid = defaultdict(dict)
            for x in range(self.x_size):
                for y in range(self.y_size):
                    current = self.grid[x][y]
                    adjacent = Counter(self.adjacent_points(x, y))

                    #  Open rules
                    if current == OPEN_SPACE:
                        if adjacent[TREES] >= 3:
                            iterated = TREES
                        else:
                            iterated = OPEN_SPACE

                    #  Tree rules
                    elif current == TREES:
                        if adjacent[LUMBERYARD] >= 3:
                            iterated = LUMBERYARD
                        else:
                            iterated = TREES

                    #  Lumberyard rules
                    elif current == LUMBERYARD:
                        if adjacent[TREES] and adjacent[LUMBERYARD]:
                            iterated = LUMBERYARD
                        else:
                            iterated = OPEN_SPACE

                    else:
                        raise

                    new_grid[x][y] = iterated

            self.grid = new_grid

        return self


if __name__ == "__main__":
    data = get_data(year=2018, day=18)
    print("Problem 1:", Lumberyard(data).iterate(10).value)
    print("Problem 2:", "Eyeballed from repeated values")
