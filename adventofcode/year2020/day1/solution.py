import operator
from dataclasses import dataclass
from functools import reduce
from itertools import permutations

from aocd.models import Puzzle


@dataclass
class ExpenseReport:
    expenses: list
    tuple_size: int = 2

    @property
    def product_2020(self):
        """Return the product of two expenses that sum to 2020."""
        for p in permutations(self.expenses, r=self.tuple_size):
            if sum(p) == 2020:
                return reduce(operator.mul, p)

        raise ValueError("Expected a permutation that summed to 2020")


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=1)
    expenses = [int(m) for m in puzzle.input_data.split("\n")]
    puzzle.answer_a = ExpenseReport(expenses).product_2020
    puzzle.answer_b = ExpenseReport(expenses, tuple_size=3).product_2020
