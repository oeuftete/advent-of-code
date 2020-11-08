from functools import total_ordering


@total_ordering
class Coordinate:
    def __init__(self, x=0, y=0, csv=None):
        if csv:
            (self.x, self.y) = map(int, csv.replace(" ", "").split(","))
        else:
            self.x = x
            self.y = y

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.x, self.y))

    def is_bounded_by(self, other, direction):
        if direction == "east":
            return self.x < other.x and (other.x - self.x) >= abs(self.y - other.y)
        elif direction == "west":
            return self.x > other.x and (self.x - other.x) >= abs(self.y - other.y)
        elif direction == "north":
            return self.y < other.y and (other.y - self.y) >= abs(self.x - other.x)
        elif direction == "south":
            return self.y > other.y and (self.y - other.y) >= abs(self.x - other.x)

        raise ValueError
