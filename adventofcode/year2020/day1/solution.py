import operator
from functools import reduce
from itertools import permutations

from aocd.models import Puzzle
from cached_property import cached_property


class ExpenseReport:
    def __init__(self, expenses, tuple_size=2):
        self.expenses = expenses
        self.tuple_size = tuple_size

    @cached_property
    def product_2020(self):
        """Return the product of two expenses that sum to 2020."""
        for p in permutations(self.expenses, r=self.tuple_size):
            if reduce(operator.add, p) == 2020:
                return reduce(operator.mul, p)


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=1)
    expenses = [int(m) for m in puzzle.input_data.split("\n")]
    puzzle.answer_a = ExpenseReport(expenses).product_2020
    puzzle.answer_b = ExpenseReport(expenses, tuple_size=3).product_2020
