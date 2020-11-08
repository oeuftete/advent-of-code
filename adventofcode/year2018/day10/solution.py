import logging
import math
import re
from collections import defaultdict

from aocd import get_data


def parse_point_and_vector(s):
    int_re = r"(\s*\-?\d+)"
    POINT_FORMAT = r"position=<%s,%s> velocity=<%s,%s>$" % (
        int_re,
        int_re,
        int_re,
        int_re,
    )
    m = re.match(POINT_FORMAT, s)
    (x, y, dx, dy) = list(map(int, m.groups()))
    return (x, y, dx, dy)


def data_to_sky(data):
    return Sky(
        list(
            map(
                lambda p: SkyPoint(*p), map(lambda ps: parse_point_and_vector(ps), data)
            )
        )
    )


class SkyPoint:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy


class Sky:
    def __init__(self, points):
        self.points = points
        self._build_sky()

    def _build_sky(self):
        self.sky = defaultdict(lambda: defaultdict(lambda: "."))
        self.min_x = self.min_y = math.inf
        self.max_x = self.max_y = -math.inf
        for p in self.points:
            self.sky[p.x][p.y] = "#"
            self.max_x = p.x if p.x > self.max_x else self.max_x
            self.max_y = p.y if p.y > self.max_y else self.max_y
            self.min_x = p.x if p.x < self.min_x else self.min_x
            self.min_y = p.y if p.y < self.min_y else self.min_y

    def iterate(self, n=1):
        for _ in range(n):
            for p in self.points:
                p.move()
        self._build_sky()
        return self

    def dump_sky(self, max_width=1000, max_height=1000):
        s = ""
        width = self.max_x - self.min_x
        height = self.max_y - self.min_y
        logging.debug("Area = (%d x %d)" % (width, height))
        if width <= max_width and height <= max_height:
            for y in range(self.min_y, self.max_y + 1):
                for x in range(self.min_x, self.max_x + 1):
                    s += self.sky[x][y]
                s += "\n"
            return s


if __name__ == "__main__":
    data = get_data(year=2018, day=10).split("\n")
    print("Problem 1:", "Use local_run.py")
    print("Problem 2:", "Use local_run.py")
