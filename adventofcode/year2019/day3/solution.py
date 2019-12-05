import logging
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

    @property
    def length(self):
        return self.start.manhattan_distance(self.end)

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


def closest_intersection(path_one, path_two, use_steps=False):
    wires = [Wire(), Wire()]

    for i, path in enumerate([path_one, path_two]):
        for move in path.split(','):
            wires[i].add_line(move)

    # Now look at each line in wire 0, and find its intersections with wire 1's
    # lines.
    intersections = list()
    intersection_steps = list()

    path_one_step_count = 0
    for line_path_one in wires[0].lines:
        path_two_step_count = 0
        for line_path_two in wires[1].lines:
            intersection = line_path_one.intersection(line_path_two)

            if not intersection:
                path_two_step_count += line_path_two.length
                logging.debug(
                    f'... path two step count is {path_two_step_count}')
                continue

            logging.debug(f'Found intersection {intersection}')
            intersections.append(intersection)

            step_count = (
                path_one_step_count +
                line_path_one.start.manhattan_distance(intersection) +
                path_two_step_count +
                line_path_two.start.manhattan_distance(intersection))
            logging.debug(f'... step count is {step_count}')
            intersection_steps.append(step_count)

            path_two_step_count += line_path_two.length
            logging.debug(f'... path two step count is {path_two_step_count}')

        path_one_step_count += line_path_one.length
        logging.debug(f'... path one step count is {path_one_step_count}')

    optimum = math.inf

    for i, intersection in enumerate(intersections):
        distance = intersection.manhattan_distance(wires[0].origin)

        #  Ignore origin overlap.
        if distance == 0:
            continue

        if use_steps:
            optimum = min(intersection_steps[i], optimum)
        else:
            optimum = min(distance, optimum)

    return optimum
