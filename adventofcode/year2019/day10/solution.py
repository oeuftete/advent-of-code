from fractions import Fraction
import logging
import math

from adventofcode.common.coordinate import Coordinate


class Line(object):
    #  Has two coordinates.
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    @property
    def points_on_line(self):
        #  Find all coordinates exactly on the line.
        result = list()
        c1, c2 = self.c1, self.c2

        if c1 == c2:
            return result

        m = None
        b = None

        x_big, x_little = (c1.x, c2.x) if c1.x > c2.x else (c2.x, c1.x)
        y_big, y_little = (c1.y, c2.y) if c1.y > c2.y else (c2.y, c1.y)
        x_range = range(x_little + 1, x_big)
        y_range = range(y_little + 1, y_big)

        try:
            m = Fraction((c2.y - c1.y), (c2.x - c1.x))
            b = c1.y - m * c1.x
            assert b == c2.y - m * c2.x
        except ZeroDivisionError:
            logging.debug('Vertical line...')
            result.extend([Coordinate(c1.x, y) for y in y_range])
            return result

        logging.debug(f'Line = {m}x + {b}')
        if m == 0:
            logging.debug('Horizontal line...')
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

        logging.debug(f'Result = {result}')
        return result


class Asteroid(Coordinate):
    def __init__(self, *args, **kwargs):
        super(Asteroid, self).__init__(*args, **kwargs)
        self.viewable_asteroids = set()

    def add_viewable(self, other):
        assert isinstance(other, Asteroid)
        self.viewable_asteroids.add(other)

    @property
    def n_viewable(self):
        logging.debug('Viewable = ' f'{self.viewable_asteroids}')
        return len(self.viewable_asteroids)


class AsteroidMap(object):
    EMPTY = '.'
    ASTEROID = '#'

    def __init__(self, input_data):
        self.asteroids = list()
        self._build_asteroids(input_data)  # make lazy?
        self._build_views()  # make lazy?

    def _build_asteroids(self, input_data):
        # The asteroids can be described with X,Y coordinates where X is the
        # distance from the left edge and Y is the distance from the top edge
        # (so the top-left corner is 0,0 and the position immediately to its
        # right is 1,0).
        for (y, l) in enumerate(input_data.split('\n')):
            for (x, c) in enumerate(l):
                if c == self.ASTEROID:
                    self.asteroids.append(Asteroid(x, y))

    def has_asteroid_at(self, c):
        return c in self.asteroids

    def get_asteroid_at(self, c):
        for a in self.asteroids:
            if a == c:
                return a

    def _build_views(self):
        for i, a1 in enumerate(self.asteroids):
            logging.debug(f'Checking {a1} ...')
            for a2 in self.asteroids[i + 1:]:
                logging.debug(f'... against {a2} ...')
                line = Line(a1, a2)
                for c in line.points_on_line + [a2]:
                    logging.debug(f'... checking point on line {c}...')
                    if self.has_asteroid_at(Coordinate(c.x, c.y)):
                        a_seen = self.get_asteroid_at(Coordinate(c.x, c.y))
                        logging.debug(f'*** Can see: {a1} <--> {a_seen}')
                        a1.add_viewable(a_seen)
                        a_seen.add_viewable(a1)
                        break

    @property
    def best_asteroid(self):
        max_viewable = -math.inf
        best_asteroid = None

        for asteroid in self.asteroids:
            logging.debug(f'Checking asteroid {asteroid}...')
            if asteroid.n_viewable > max_viewable:
                max_viewable = asteroid.n_viewable
                best_asteroid = asteroid
                logging.debug(f'*** New best: {best_asteroid}')
                logging.debug(' ** Can see:  '
                              f'{best_asteroid.viewable_asteroids}')

        return best_asteroid
