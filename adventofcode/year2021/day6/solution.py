import typing
from collections import Counter

import attr
from aocd.models import Puzzle  # type: ignore

from adventofcode.common.utils import list_str_to_int


@attr.s
class School:
    fish: typing.List[int] = attr.ib(converter=list_str_to_int)
    fish_counter: Counter = attr.ib(init=False, factory=Counter)

    def __attrs_post_init__(self):
        self.fish_counter = Counter(self.fish)

    def age(self, n=1):
        for _ in range(n):
            for i, age in enumerate(self.fish.copy()):
                if age > 0:
                    self.fish[i] -= 1
                elif age == 0:
                    self.fish[i] = 6
                    self.fish.append(8)

    def smart_age(self, n=1):
        for _ in range(n):
            new_counter = Counter()
            for i in range(9):
                c_i = self.fish_counter[i]
                if i == 0:
                    new_counter[8] = c_i
                    new_counter[6] += c_i
                else:
                    new_counter[i - 1] += c_i
            self.fish_counter = new_counter


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=6)
    school = School(puzzle.input_data.strip().split(","))
    #  school.age(80)
    #  puzzle.answer_a = len(school.fish)
    school.smart_age(80)
    puzzle.answer_a = school.fish_counter.total()
    school.smart_age(256 - 80)
    puzzle.answer_b = school.fish_counter.total()
