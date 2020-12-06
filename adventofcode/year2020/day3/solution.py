import logging

from aocd.models import Puzzle

from adventofcode.common.coordinate import Coordinate

logging.basicConfig(level=logging.INFO)


class TreedSlope:

    TREE = "#"

    def __init__(self, slope_map):
        self.slope_map = slope_map
        self.trees_hit = 0
        self._build_slope()

    def _build_slope(self):
        self.width = self.height = 0
        self.trees = []
        for (y, l) in enumerate(self.slope_map.split("\n")):
            self.height += 1
            self.width = len(l)
            for (x, c) in enumerate(l):
                if c == self.TREE:
                    self.trees.append(Coordinate(x, y))

    def is_tree_at(self, x, y):
        if y > self.height - 1:
            raise ValueError("Coordinate off of grid")
        x %= self.width
        logging.debug("Trees = %s", self.trees)
        logging.debug("x = %s", x)
        return Coordinate(x, y) in self.trees

    def slide(self, dx=3, dy=1):
        x = y = 0
        try:
            while True:
                x += dx
                y += dy
                if self.is_tree_at(x, y):
                    self.trees_hit += 1
        except ValueError:
            pass

    def go_back_to_the_top(self):
        self.trees_hit = 0

    def multiple_slide_product(self, tuples):
        product = 1
        for t in tuples:
            self.go_back_to_the_top()
            self.slide(t[0], t[1])
            product *= self.trees_hit

        return product


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=3)
    slope = TreedSlope(puzzle.input_data)
    slope.slide()
    puzzle.answer_a = slope.trees_hit
    puzzle.answer_b = slope.multiple_slide_product(
        [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    )
