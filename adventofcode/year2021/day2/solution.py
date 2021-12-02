import re
import typing

import attr
from aocd.models import Puzzle


@attr.s
class Positionator:
    course: typing.List[str] = attr.ib()
    course_type: str = attr.ib(default="position")
    forward: int = attr.ib(default=0, init=False)
    depth: int = attr.ib(default=0, init=False)
    aim: int = attr.ib(default=0, init=False)

    def __attrs_post_init__(self):
        if self.course_type == "position":
            self._process_position_commands()
        elif self.course_type == "aim":
            self._process_aim_commands()
        else:
            raise ValueError("Bad course type!")

    def _process_position_commands(self):
        for command in self.course:
            m = re.match(r"(forward|up|down) (\d+)", command)
            direction, units = m.groups()
            units = int(units)
            if direction == "forward":
                self.forward += units
            elif direction == "up":
                self.depth -= units
            elif direction == "down":
                self.depth += units
            else:
                raise ValueError("Bad command!")

    def _process_aim_commands(self):
        for command in self.course:
            m = re.match(r"(forward|up|down) (\d+)", command)
            direction, units = m.groups()
            units = int(units)
            if direction == "forward":
                self.forward += units
                self.depth += self.aim*units
            elif direction == "up":
                self.aim -= units
            elif direction == "down":
                self.aim += units
            else:
                raise ValueError("Bad command!")

    @property
    def position_product(self):
        return self.forward * self.depth


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=2)
    course = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = Positionator(course).position_product
    puzzle.answer_b = Positionator(course, course_type="aim").position_product
