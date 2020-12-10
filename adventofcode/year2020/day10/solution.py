import logging
from collections import Counter
from dataclasses import dataclass, field

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class AdapterBag:
    bag: list
    diffs: Counter = field(init=False, default_factory=Counter)

    def chain(self):
        joltage = 0
        for adapter in sorted(self.bag):
            logging.debug("Checking adapter [%s], current j = [%s]", adapter, joltage)
            diff = adapter - joltage
            if diff > 3:
                raise ValueError(f"Unexpectedly large diff found: {diff}")

            self.diffs[diff] += 1
            joltage = adapter

        #  Add device built-in
        self.diffs[3] += 1

        logging.debug(self.diffs)

    def diffs_product(self):
        return self.diffs[1] * self.diffs[3]


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=10)
    bag_list = [int(m) for m in puzzle.input_data.strip().splitlines()]
    bag = AdapterBag(bag_list)
    bag.chain()
    puzzle.answer_a = bag.diffs_product()
