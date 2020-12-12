import itertools
import math
from collections import deque
from dataclasses import dataclass, field

from aocd.models import Puzzle

from adventofcode.common.coordinate import Coordinate


@dataclass
class NavSystem:
    instructions: list
    instruction_queue: deque = field(init=False)
    bearing: str = "east"
    origin: Coordinate = field(default_factory=Coordinate)
    location: Coordinate = field(init=False)

    def __post_init__(self):
        self.location = Coordinate(self.origin.x, self.origin.y)
        self.instruction_queue = deque(self.instructions)

    def process(self, n=math.inf):
        for i in itertools.count(start=1):
            if i > n:
                return

            try:
                instruction = self.instruction_queue.popleft()
            except IndexError:
                break
            action, value = instruction[0], instruction[1:]
            self.perform_action(action, int(value))

    def perform_action(self, action, value):
        if action in "NESW":
            self.move_direction(action, value)
        if action == "F":
            self.move_direction(self.bearing.capitalize()[0], value)
        if action in "RL":
            self.change_bearing(action, value)

    def move_direction(self, direction, value):
        if direction == "N":
            self.location.y += value
        if direction == "S":
            self.location.y -= value
        if direction == "E":
            self.location.x += value
        if direction == "W":
            self.location.x -= value

    def change_bearing(self, turn, value):
        bearings = ["north", "east", "south", "west"]
        current_index = bearings.index(self.bearing)
        i = int(value / 90)
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
