from collections import defaultdict
from functools import total_ordering
import itertools
import logging

from aocd import get_data

logging.basicConfig(level=logging.INFO)


@total_ordering
class Cart:

    #  sorted() order
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)

    def __init__(self, c, x, y):
        self.x = x
        self.y = y
        self._build_vector(c)

        self.intersection_vectors = itertools.cycle(
            [lambda c: c.turn_left(), lambda c: c.vector, lambda c: c.turn_right()]
        )

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def _build_vector(self, c):
        if c == ">":
            self.vector = Cart.RIGHT
        elif c == "<":
            self.vector = Cart.LEFT
        elif c == "^":
            self.vector = Cart.UP
        elif c == "v":
            self.vector = Cart.DOWN

    def move(self):
        self.x += self.vector[0]
        self.y += self.vector[1]

    def turn_left(self):
        (dx, dy) = self.vector
        new_vector = None
        if dx:
            new_vector = (0, -1 * dx)
        else:
            new_vector = (1 * dy, 0)

        return new_vector

    def turn_right(self):
        (dx, dy) = self.vector
        new_vector = None
        if dx:
            new_vector = (0, 1 * dx)
        else:
            new_vector = (-1 * dy, 0)

        return new_vector

    def update_vector(self, tile):
        v = self.vector

        logging.debug("update_vector: tile={}; v={}".format(tile, v))

        if tile == "+":
            #  TODO: A tad clunky
            self.vector = next(self.intersection_vectors)(self)
        elif tile == "/":
            if v in [Cart.LEFT, Cart.RIGHT]:
                self.vector = self.turn_left()
            else:
                self.vector = self.turn_right()
        elif tile == "\\":
            if v in [Cart.LEFT, Cart.RIGHT]:
                self.vector = self.turn_right()
            else:
                self.vector = self.turn_left()
        elif tile == " ":
            raise OffTheRailsException

    @property
    def position(self):
        return (self.x, self.y)


class TrackCollision(Exception):
    def __init__(self, position):
        self.position = position


class OffTheRailsException(Exception):
    pass


class Track:
    def __init__(self, grid_string):
        self.carts = list()
        self.grid = self._parse_grid(grid_string)
        self.collision_position = None
        self.iterations = 0
        self.crash_ends = True

    @property
    def cart_positions(self):
        return [c.position for c in self.carts]

    @property
    def cart_vectors(self):
        return [c.vector for c in self.carts]

    def grid_square(self, x, y):
        return self.grid[x][y]

    def _parse_grid(self, s):
        g = defaultdict(lambda: defaultdict(lambda: " "))

        row = 0
        for l in s.split("\n"):
            col = 0
            for c in l:
                if c == ">" or c == "<":
                    g[col][row] = "-"
                    self.carts.append(Cart(c, col, row))
                elif c == "^" or c == "v":
                    g[col][row] = "|"
                    self.carts.append(Cart(c, col, row))
                else:
                    g[col][row] = c

                col += 1

            row += 1

        return g

    def check_for_collisions(self):
        positions = list()
        for c in self.carts:
            p = c.position
            if p in positions:
                self.collision_position = p
                raise TrackCollision(p)

            positions.append(p)

        return False

    def clean_up_collision(self, position):
        self.carts = [c for c in self.carts if c.position != position]

    def iterate(self):
        self.iterations += 1
        invalidated_start_positions = list()

        for c in [c for c in sorted(self.carts)]:
            if c.position in invalidated_start_positions:
                logging.debug(
                    "Not moving cart at {}:{}, it collided...".format(c.x, c.y)
                )
                continue

            logging.debug(
                "Moving cart at {}:{}, vector {}...".format(c.x, c.y, c.vector)
            )
            c.move()
            new_tile = self.grid_square(c.x, c.y)
            c.update_vector(new_tile)
            logging.debug(
                "Moved cart to {}:{}, tile [{}], new vector {}...".format(
                    c.x, c.y, new_tile, c.vector
                )
            )
            try:
                self.check_for_collisions()
            except TrackCollision as e:
                logging.info("[{}] Collision at {}".format(self.iterations, e.position))
                if self.crash_ends:
                    raise
                else:
                    logging.info(
                        "[{}] Cleaning up collision at {}".format(
                            self.iterations, e.position
                        )
                    )
                    self.clean_up_collision(e.position)
                    invalidated_start_positions.append(e.position)

        return self

    def run(self):
        for _ in itertools.count():
            try:
                self.iterate()
            except TrackCollision:
                return

            if len(self.carts) <= 1:
                return


if __name__ == "__main__":
    grid_string = get_data(year=2018, day=13)
    track = Track(grid_string)
    track.run()
    print("Problem 1:", track.collision_position, track.iterations)

    clean_track = Track(grid_string)
    clean_track.crash_ends = False
    clean_track.run()
    print("Problem 2:", clean_track.carts[0].position, clean_track.iterations)
