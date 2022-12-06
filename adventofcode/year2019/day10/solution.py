import logging
import math
from fractions import Fraction
from functools import cached_property

import attr

from adventofcode.common.coordinate import Coordinate


class Line:
    #  Has two coordinates.
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    @property
    def equation(self):
        c1, c2 = self.c1, self.c2
        m = b = None
        try:
            m = Fraction((c2.y - c1.y), (c2.x - c1.x))
            b = c1.y - m * c1.x
            assert b == c2.y - m * c2.x
        except ZeroDivisionError:
            logging.debug("Vertical line...")
            m = math.inf

        logging.debug("Line = %fx + %f", m, b)
        return (m, b)

    @property
    def points_on_line(self):
        #  Find all coordinates exactly on the line.
        result = []
        c1, c2 = self.c1, self.c2

        if c1 == c2:
            return result

        (m, b) = self.equation

        x_big, x_little = (c1.x, c2.x) if c1.x > c2.x else (c2.x, c1.x)
        y_big, y_little = (c1.y, c2.y) if c1.y > c2.y else (c2.y, c1.y)
        x_range = range(x_little + 1, x_big)
        y_range = range(y_little + 1, y_big)

        if math.isinf(m):
            result.extend([Coordinate(c1.x, y) for y in y_range])

        if m == 0:
            logging.debug("Horizontal line...")
            result.extend([Coordinate(x, c1.y) for x in x_range])

        if m < 1:
            for y in y_range:
                x = Fraction((y - b), m)
                if x.denominator == 1:
                    result.append(Coordinate(x, y))
        else:
            for x in x_range:
                y = m * x + b
                if y.denominator == 1:
                    result.append(Coordinate(x, y))

        logging.debug("Result = %s", result)
        return result


@attr.s
class Asteroid(Coordinate):
    viewable_asteroids = attr.ib(factory=set, cmp=False, init=False, repr=False)

    def add_viewable(self, other):
        assert isinstance(other, Asteroid)
        self.viewable_asteroids.add(other)

    @property
    def n_viewable(self):
        logging.debug("Viewable = %s", self.viewable_asteroids)
        return len(self.viewable_asteroids)


class AsteroidMap:
    EMPTY = "."
    ASTEROID = "#"

    def __init__(self, input_data):
        self.asteroids = []
        self._build_asteroids(input_data)  # make lazy?
        self._build_views()  # make lazy?
        self.vaporized = []

    def _build_asteroids(self, input_data):
        # The asteroids can be described with X,Y coordinates where X is the
        # distance from the left edge and Y is the distance from the top edge
        # (so the top-left corner is 0,0 and the position immediately to its
        # right is 1,0).
        self.width = self.height = 0
        for (y, l) in enumerate(input_data.split("\n")):
            self.height += 1
            self.width = len(l)
            for (x, c) in enumerate(l):
                if c == self.ASTEROID:
                    self.asteroids.append(Asteroid(x, y))

    def has_asteroid_at(self, c):
        return c in map(lambda a: Coordinate(*(a.x, a.y)), self.asteroids)

    def get_asteroid_at(self, c):
        for a in self.asteroids:
            if (a.x, a.y) == (c.x, c.y):
                return a

    def remove_asteroid_at(self, c):
        for i, a in enumerate(self.asteroids):
            if (a.x, a.y) == (c.x, c.y):
                del self.asteroids[i : i + 1]
                return True

        return False

    def _build_views(self):
        for i, a1 in enumerate(self.asteroids):
            logging.debug("Checking %s ...", a1)
            for a2 in self.asteroids[i + 1 :]:
                logging.debug("... against %s ...", a2)
                line = Line(a1, a2)
                for c in line.points_on_line + [a2]:
                    logging.debug("... checking point on line %s...", c)
                    if self.has_asteroid_at(Coordinate(c.x, c.y)):
                        a_seen = self.get_asteroid_at(Coordinate(c.x, c.y))
                        logging.debug("*** Can see: %s <--> %s", a1, a_seen)
                        a1.add_viewable(a_seen)
                        a_seen.add_viewable(a1)
                        break

    @cached_property
    def best_asteroid(self):
        max_viewable = -math.inf
        best_asteroid = None

        for asteroid in self.asteroids:
            logging.debug("Checking asteroid %s...", asteroid)
            if asteroid.n_viewable > max_viewable:
                max_viewable = asteroid.n_viewable
                best_asteroid = asteroid
                logging.debug("*** New best: %s", best_asteroid)
                logging.debug(" ** Can see:  %s", best_asteroid.viewable_asteroids)

        return best_asteroid

    @property
    def station(self):
        return self.best_asteroid

    @property
    def equations_from_station(self):
        """
        Build a set of all possible lines from the station to other points on
        the map.
        """
        station_equations = set()
        for x in range(self.width):
            for y in range(self.height):
                line = Line(self.station, Coordinate(x, y))
                station_equations.add(line.equation)

        return station_equations

    def zap(self, x, y):
        zapped = self.remove_asteroid_at(Coordinate(x, y))
        if zapped:
            self.vaporized.append(Asteroid(x, y))
            logging.debug("Zapped (%s, %s)", x, y)
        return zapped

    def run_vaporizer(self, limit=None):
        self.vaporized = list()
        limit = limit or math.inf

        positive = sorted(
            [
                eq[0]
                for eq in self.equations_from_station
                if (eq[0] > 0 and not math.isinf(eq[0]))
            ]
        )
        negative = sorted(
            [
                eq[0]
                for eq in self.equations_from_station
                if (eq[0] < 0 and not math.isinf(eq[0]))
            ]
        )

        sx, sy = self.station.x, self.station.y
        while len(self.vaporized) < limit:

            last_count = len(self.asteroids)

            #  Look straight up
            for y in reversed(range(0, sy)):
                if self.zap(sx, y):
                    break

            #  TODO: A lot of near-repetition here.  Fix!
            #  Check the negative slopes, looking up (-y) and right (+x)
            for slope in negative:
                logging.debug(
                    f"NE: Checking slope {slope} from station ({sx}, {sy})..."
                )
                if abs(slope) > 1:
                    for x in range(sx + 1, self.width):
                        y = sy - (slope * (sx - x))
                        logging.debug(f".... checking zap: ({x}, {y})")
                        if y < 0:
                            break
                        if y.denominator != 1:
                            continue
                        if self.zap(x, y):
                            break
                else:
                    for y in reversed(range(0, sy)):
                        x = sx - (1 / slope) * (sy - y)
                        logging.debug(f".... checking zap: ({x}, {y})")
                        if x > self.width:
                            break
                        if x.denominator != 1:
                            continue
                        if self.zap(x, y):
                            break

            #  Look right
            logging.debug(f"E: Checking slope {slope} from station ({sx}, {sy})...")
            for x in range(sx + 1, self.width):
                if self.zap(x, sy):
                    break

            #  Check the positive slopes, looking down (+y) and right (+x)
            for slope in positive:
                logging.debug(
                    f"SE: Checking slope {slope} from station ({sx}, {sy})..."
                )
                if slope > 1:
                    for x in range(sx + 1, self.width):
                        y = sy - (slope * (sx - x))
                        logging.debug(f".... checking zap: ({x}, {y})")
                        if y < 0:
                            break
                        if y.denominator != 1:
                            continue
                        if self.zap(x, y):
                            break
                else:
                    for y in range(sy + 1, self.height):
                        x = sx - (1 / slope) * (sy - y)
                        logging.debug(f".... checking zap: ({x}, {y})")
                        if x > self.width:
                            break
                        if x.denominator != 1:
                            continue
                        if self.zap(x, y):
                            break

            #  Look straight down
            logging.debug(f"S: Checking slope {slope} from station ({sx}, {sy})...")
            for y in range(sy + 1, self.height):
                if self.zap(sx, y):
                    break

            #  Check the negative slopes, looking down (+y) and left (-x)
            for slope in negative:
                logging.debug(
                    f"SW: Checking slope {slope} from station ({sx}, {sy})..."
                )
                if slope > 1:
                    for x in reversed(range(0, sx)):
                        y = sy - (slope * (sx - x))
                        logging.debug(f".... checking zap: ({x}, {y})")
                        if y > self.height:
                            break
                        if y.denominator != 1:
                            continue
                        if self.zap(x, y):
                            break
                else:
                    for y in range(sy + 1, self.height):
                        x = sx - (1 / slope) * (sy - y)
                        logging.debug(f".... checking zap: ({x}, {y})")
                        if x < 0:
                            break
                        if x.denominator != 1:
                            continue
                        if self.zap(x, y):
                            break

            #  Look left
            logging.debug(f"W: Checking slope {slope} from station ({sx}, {sy})...")
            for x in reversed(range(0, sx)):
                if self.zap(x, sy):
                    break

            #  Check the positive slopes, looking up (-y) and left (-x)
            for slope in positive:
                logging.debug(
                    f"NW: Checking slope {slope} from station ({sx}, {sy})..."
                )
                if abs(slope) > 1:
                    for x in reversed(range(0, sx)):
                        y = sy - (slope * (sx - x))
                        logging.debug(f".... checking zap: ({x}, {y})")
                        if y < 0:
                            break
                        if y.denominator != 1:
                            continue
                        if self.zap(x, y):
                            break
                else:
                    for y in reversed(range(0, sy)):
                        x = sx - (1 / slope) * (sy - y)
                        logging.debug(f".... checking zap: ({x}, {y})")
                        if x < 0:
                            break
                        if x.denominator != 1:
                            continue
                        if self.zap(x, y):
                            break

            if len(self.asteroids) == last_count:
                logging.warning("No asteroids found to zap!")
                break
