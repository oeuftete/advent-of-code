from itertools import permutations

from aocd.models import Puzzle
from cached_property import cached_property


class ExpenseReport:
    def __init__(self, expenses):
        self.expenses = expenses

    @cached_property
    def product_2020(self):
        """Return the product of two expenses that sum to 2020."""
        for p in permutations(self.expenses, r=2):
            if p[0] + p[1] == 2020:
                return p[0] * p[1]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=1)
    expenses = [int(m) for m in puzzle.input_data.split("\n")]
    puzzle.answer_a = ExpenseReport(expenses).product_2020
