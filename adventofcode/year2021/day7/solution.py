import math

import attr
from aocd.models import Puzzle  # type: ignore

from adventofcode.common.utils import list_str_to_int


@attr.s
class CrabAligner:
    positions: list[int] = attr.ib(converter=list_str_to_int)
    is_escalating_fuel_cost: bool = attr.ib(default=False)

    @property
    def alignment_fuel_expenditure(self) -> int:
        min_fuel_used = math.inf

        for i in range(min(self.positions), max(self.positions) + 1):
            fuel_used = 0
            for pos in self.positions:
                if self.is_escalating_fuel_cost:
                    fuel_used += sum(range(abs(i - pos) + 1))
                else:
                    fuel_used += abs(i - pos)

            min_fuel_used = min(min_fuel_used, fuel_used)

        return int(min_fuel_used)


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=7)
    positions = puzzle.input_data.strip().split(",")
    puzzle.answer_a = CrabAligner(positions).alignment_fuel_expenditure
    puzzle.answer_b = CrabAligner(
        positions, is_escalating_fuel_cost=True
    ).alignment_fuel_expenditure
