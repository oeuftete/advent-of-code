import logging
from functools import cached_property

import attr
from aocd.models import Puzzle

from adventofcode.common.coordinate import Coordinate

logging.basicConfig(level=logging.INFO)


@attr.s
class Tree:
    coordinate: Coordinate = attr.ib()
    height: int = attr.ib()
    boundary: Coordinate = attr.ib(init=False)


@attr.s
class TreeSpotter:
    map: str = attr.ib()
    tree_map: list[list[Tree]] = attr.ib(factory=list, init=False)
    boundary: Coordinate = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self.read_map()

    def read_map(self) -> None:
        """Parse the forest map into Trees"""
        max_x = max_y = 0
        for y, row in enumerate(self.map.splitlines()):
            self.tree_map.append([])
            max_y = max(max_y, y)
            for x, t in enumerate(row):
                logging.debug("Adding Tree at (%d,%d) of height [%s]", x, y, t)
                self.tree_map[y].append(Tree(Coordinate(x, y), int(t)))
                max_x = max(max_x, x)

        self.boundary = Coordinate(max_x, max_y)

    @classmethod
    def all_visible(cls, obscurers: list[Tree], tree: Tree):
        return all((t.height < tree.height for t in obscurers))

    def tree_is_visible(self, x: int, y: int) -> bool:
        if x == 0 or y == 0 or x == self.boundary.x or y == self.boundary.y:
            return True

        this_tree = self.tree_map[y][x]

        # Look at each of self.tree_map[y][x] for given y, and x from 0 to x,
        # and x+1 to x_bound.  Are all of those <h? If so, return True.
        if self.all_visible(self.tree_map[y][:x], this_tree):
            return True
        if self.all_visible(self.tree_map[y][x + 1 :], this_tree):
            return True

        # Look at each of self.tree_map[y][x] for given x, and y from 0 to y,
        # and y+1 to y_bound.  Are all of those <h? If so, return True.
        y_upper = []
        for iy in range(0, y):
            y_upper.append(self.tree_map[iy][x])
        if self.all_visible(y_upper, this_tree):
            return True

        y_lower = []
        for iy in range(y + 1, self.boundary.y + 1):
            y_lower.append(self.tree_map[iy][x])
        if self.all_visible(y_lower, this_tree):
            return True

        return False

    @cached_property
    def part_a_solution(self) -> int:
        n_visible = 0
        for iy, tree_row in enumerate(self.tree_map):
            for ix, _ in enumerate(tree_row):
                if self.tree_is_visible(ix, iy):
                    n_visible += 1

        return n_visible

    def scenic_score(self, x: int, y: int) -> int:
        # For each direction, iterate through the list until running out of
        # trees, or a tree is higher than the tree at x,y.  Capture the
        # number of trees seen once the condition fails.  Multiply all four
        # together to get the final score.
        scenic_score = 1
        this_height = self.tree_map[y][x].height

        logging.debug(
            "Looking for trees from [%d, %d] at height [%d]", x, y, this_height
        )

        # up
        local_seen = 0
        for iy in reversed(range(0, y)):
            local_seen = local_seen + 1
            seen_height = self.tree_map[iy][x].height
            logging.debug(
                "(up) Saw a tree at [%d, %d] with height [%d]", x, iy, seen_height
            )
            if seen_height >= this_height:
                break

        scenic_score = scenic_score * local_seen

        # down
        local_seen = 0
        for iy in range(y + 1, self.boundary.y + 1):
            local_seen = local_seen + 1
            seen_height = self.tree_map[iy][x].height
            logging.debug(
                "(down) Saw a tree at [%d, %d] with height [%d]", x, iy, seen_height
            )
            if seen_height >= this_height:
                break

        scenic_score = scenic_score * local_seen

        # left
        local_seen = 0
        for ix in reversed(range(0, x)):
            local_seen = local_seen + 1
            seen_height = self.tree_map[y][ix].height
            logging.debug(
                "(left) Saw a tree at [%d, %d] with height [%d]", ix, y, seen_height
            )
            if seen_height >= this_height:
                break

        scenic_score = scenic_score * local_seen

        # right
        local_seen = 0
        for ix in range(x + 1, self.boundary.x + 1):
            local_seen = local_seen + 1
            seen_height = self.tree_map[y][ix].height
            logging.debug(
                "(right) Saw a tree at [%d, %d] with height [%d]", ix, y, seen_height
            )
            if seen_height >= this_height:
                break

        scenic_score = scenic_score * local_seen

        return scenic_score

    @cached_property
    def part_b_solution(self) -> int:
        scenic_score = 0

        #  Ignore the edges since they will always have a direction with 0,
        #  and so a scenic score of 0.
        for iy, tree_row in list(enumerate(self.tree_map))[1:-1]:
            for ix, _ in list(enumerate(tree_row))[1:-1]:
                this_score = self.scenic_score(ix, iy)
                logging.debug("Found scenic score [%d] at [%d,%d]", this_score, ix, iy)
                scenic_score = max(scenic_score, this_score)

        return scenic_score


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=8)
    tree_spotter = TreeSpotter(puzzle.input_data.strip())
    puzzle.answer_a = tree_spotter.part_a_solution
    puzzle.answer_b = tree_spotter.part_b_solution
