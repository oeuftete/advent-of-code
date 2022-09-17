import typing

import attr
from aocd.models import Puzzle  # type: ignore

from adventofcode.common.coordinate import Coordinate


@attr.s
class SumSpiral:
    flavour: str = attr.ib(
        default="count", validator=attr.validators.in_(["count", "neighbour"])
    )
    spiral: typing.Dict = attr.ib(init=False, default=attr.Factory(dict))
    spiral_level: int = attr.ib(init=False, default=1)
    next_coordinate: Coordinate = attr.ib(default=Coordinate(0, 0), init=False)
    next_direction: typing.Tuple = attr.ib(default=(0, 0), init=False)

    def build(self):
        # Build the spiral
        # Origin...
        # ... right 1, up 1
        # ... left 2, down 2
        # ... right 3, up 3
        # ... etc.

        #  Origin: go right
        if len(self.spiral) == 0:
            self.next_direction = (1, 0)

        # Not at the origin...
        #
        # Are we going left or right?  If so, continue in that direction as
        # many times as the spiral level.
        elif self.moving_horizontally:
            for i in range(self.spiral_level):
                self.spiral[len(self.spiral) + 1] = len(self.spiral) + 1
                # 0, 1 -> 1, 0 -> 0, -1 -> -1, 0
                self.next_direction = (self.next_direction[1], -self.next_direction[0])

        # We're going up or down.  Continue in that direction as many times as
        # the spiral level, then increase the level.
        else:
            # 1, 0 -> 1, 0 -> 0, -1 -> -1, 0
            self.next_direction = (self.next_direction[1], -self.next_direction[0])

        if self.flavour == "count":
            self.spiral[len(self.spiral) + 1] = len(self.spiral) + 1
        else:
            pass

        self.next_coordinate = Coordinate(
            self.next_coordinate.x + self.next_direction[0],
            self.next_coordinate.y + self.next_direction[1],
        )

    def moving_horizontally(self):
        return abs(self.next_direction[0]) > 0

    def moving_vertically(self):
        return abs(self.next_direction[1]) > 0

    def count_distance_to_origin(self, n):
        while len(self.spiral) < n:
            self.build()
        return self.spiral[n].manhattan_distance(self.spiral[1])

    def first_value_gt(self, n):
        return n


if __name__ == "__main__":
    puzzle = Puzzle(year=2017, day=3)
    input_datum = int(puzzle.input_data.strip())
    #  puzzle.answer_a = by inspection
    puzzle.answer_b = SumSpiral(flavour="neighbour").first_value_gt(input_datum)
