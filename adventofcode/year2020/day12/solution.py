import itertools
import math
from dataclasses import dataclass, field

from aocd.models import Puzzle

from adventofcode.common.coordinate import Coordinate


@dataclass
class NavSystem:
    instructions: list
    bearing: str = "east"
    waypoint: Coordinate = Coordinate(10, 1)
    use_waypoint: bool = False
    instruction_queue: list = field(init=False)
    origin: Coordinate = field(default_factory=Coordinate)
    location: Coordinate = field(init=False)

    def __post_init__(self):
        self.location = Coordinate(self.origin.x, self.origin.y)
        self.instruction_queue = self.instructions.copy()

    def _update_attr_from_direction(self, attribute, direction, value):
        c = getattr(self, attribute)

        if direction == "N":
            c.y += value
        if direction == "S":
            c.y -= value
        if direction == "E":
            c.x += value
        if direction == "W":
            c.x -= value

    def process(self, n=math.inf):
        for i in itertools.count(start=1):
            if i > n:
                return

            try:
                instruction = self.instruction_queue.pop(0)
            except IndexError:
                break
            action, value = instruction[0], instruction[1:]
            self.perform_action(action, int(value))

    def perform_action(self, action, value):
        if action in "NESW":
            if self.use_waypoint:
                self.move_waypoint(action, value)
            else:
                self.move_direction(action, value)
        if action == "F":
            if self.use_waypoint:
                self.move_to_waypoint(value)
            else:
                self.move_direction(self.bearing.capitalize()[0], value)
        if action in "RL":
            if self.use_waypoint:
                self.rotate_waypoint(action, value)
            else:
                self.change_bearing(action, value)

    #  WAYPOINT ACTIONS
    def move_waypoint(self, direction, value):
        self._update_attr_from_direction(
            attribute="waypoint", direction=direction, value=value
        )

    def move_to_waypoint(self, value):
        self.location.x += self.waypoint.x * value
        self.location.y += self.waypoint.y * value

    def rotate_waypoint(self, action, value):
        for _ in range(value // 90):
            wx, wy = self.waypoint.x, self.waypoint.y
            self.waypoint.x = wy if action == "R" else -wy
            self.waypoint.y = -wx if action == "R" else wx

    #  BEARING ACTIONS
    def move_direction(self, direction, value):
        self._update_attr_from_direction(
            attribute="location", direction=direction, value=value
        )

    def change_bearing(self, turn, value):
        bearings = ["north", "east", "south", "west"]
        current_index = bearings.index(self.bearing)
        i = value // 90
        if turn == "R":
            self.bearing = bearings[(current_index + i) % 4]
        if turn == "L":
            self.bearing = bearings[(current_index - i) % 4]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=12)
    instructions = puzzle.input_data.strip().splitlines()

    nav_system = NavSystem(instructions)
    nav_system.process()
    puzzle.answer_a = nav_system.location.manhattan_distance(nav_system.origin)

    nav_system = NavSystem(instructions, use_waypoint=True)
    nav_system.process()
    puzzle.answer_b = nav_system.location.manhattan_distance(nav_system.origin)
