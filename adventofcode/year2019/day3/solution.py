import math

from adventofcode.common.coordinate import Coordinate


class Line(object):
    def __init__(self, c1, c2):
        self.start = c1
        self.end = c2

    @classmethod
    def create_from_move(cls, c, move):
        move_direction = move[0]
        move_distance = int(move[1:])

        if move_direction == 'R':
            c_moved = Coordinate(x=c.x + move_distance, y=c.y)
        elif move_direction == 'L':
            c_moved = Coordinate(x=c.x - move_distance, y=c.y)
        elif move_direction == 'U':
            c_moved = Coordinate(x=c.x, y=c.y + move_distance)
        elif move_direction == 'D':
            c_moved = Coordinate(x=c.x, y=c.y - move_distance)

        return Line(c, c_moved)

    @property
    def vertical(self):
        return self.start.x == self.end.x

    @property
    def horizontal(self):
        return self.start.y == self.end.y

    def intersection(self, other):
        if ((self.horizontal and other.horizontal)
                or (self.vertical and other.vertical)):
            return None

        if self.horizontal:
            if (other.start.x in range(*sorted((self.start.x, self.end.x)))
                    and self.start.y in range(*sorted((other.start.y,
                                                       other.end.y)))):
                return Coordinate(x=other.start.x, y=self.start.y)
        else:
            if (other.start.y in range(*sorted((self.start.y, self.end.y)))
                    and self.start.x in range(*sorted((other.start.x,
                                                       other.end.x)))):
                return Coordinate(x=self.start.x, y=other.start.y)


class Wire(object):
    def __init__(self):
        self.origin = Coordinate(x=0, y=0)
        self.coordinate = self.origin
        self.lines = list()

    def add_line(self, move):
        line = Line.create_from_move(self.coordinate, move)
        self.lines.append(line)
        self.coordinate = line.end


def closest_intersection(path_one, path_two):
    wires = [Wire(), Wire()]

    for i, path in enumerate([path_one, path_two]):
        for move in path.split(','):
            wires[i].add_line(move)

    # Now look at each line in wire 0, and find its intersections with wire 1's
    # lines.
    intersections = list()
    for line_path_one in wires[0].lines:
        for line_path_two in wires[1].lines:
            intersections.append(line_path_one.intersection(line_path_two))

    closest_distance = math.inf

    for intersection in filter(lambda x: x is not None, intersections):
        distance = intersection.manhattan_distance(wires[0].origin)

        #  Ignore origin overlap.
        if distance == 0:
            continue
        closest_distance = min(distance, closest_distance)

    return closest_distance
