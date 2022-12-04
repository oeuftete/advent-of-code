import logging

import attr
from aocd.models import Puzzle
from cached_property import cached_property


@attr.s
class CalorieCounter:
    calorie_roster: str = attr.ib()
    calories: list[int] = attr.ib(factory=list, init=False)

    def __attrs_post_init__(self) -> None:
        for calorie_list in self.calorie_roster.split("\n\n"):
            logging.debug("Calorie list: %s", calorie_list)
            self.calories.append(sum(map(int, calorie_list.splitlines())))

    @cached_property
    def max_calories(self) -> int:
        return max(self.calories)

    @cached_property
    def top_three_calories(self) -> int:
        return sum(sorted(self.calories, reverse=True)[0:3])


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=1)
    calorie_counter = CalorieCounter(puzzle.input_data.strip())
    puzzle.answer_a = calorie_counter.max_calories
    puzzle.answer_b = calorie_counter.top_three_calories
