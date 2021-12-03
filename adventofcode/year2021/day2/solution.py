import typing

import attr
from aocd.models import Puzzle


@attr.s
class Positionator:
    course: typing.List[str] = attr.ib()
    course_type: str = attr.ib(
        default="position", validator=attr.validators.in_(["aim", "position"])
    )
    forward: int = attr.ib(default=0, init=False)
    depth: int = attr.ib(default=0, init=False)
    aim: int = attr.ib(default=0, init=False)

    def __attrs_post_init__(self):
        for command in self.course:
            direction, units = command.split(" ")
            units = int(units)

            match (self.course_type, direction):
                case ("position", "forward"):
                    self.forward += units
                case ("position", "up"):
                    self.depth -= units
                case ("position", "down"):
                    self.depth += units
                case ("aim", "forward"):
                    self.forward += units
                    self.depth += self.aim * units
                case ("aim", "up"):
                    self.aim -= units
                case ("aim", "down"):
                    self.aim += units

    @property
    def position_product(self):
        return self.forward * self.depth


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=2)
    course = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = Positionator(course).position_product
    puzzle.answer_b = Positionator(course, course_type="aim").position_product
