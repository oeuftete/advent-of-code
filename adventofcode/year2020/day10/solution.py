import logging
from collections import Counter
from dataclasses import dataclass, field

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class AdapterBag:
    bag: list
    diffs: Counter = field(init=False, default_factory=Counter)

    @property
    def arrangements(self):
        # Partition the bag into groups separated by at least 3
        arrangements = 1
        bag_with_zero = sorted([0] + self.bag)
        current_adapter_group_size = 0
        for i, adapter in enumerate(bag_with_zero):
            logging.debug("Checking adapter [%s], index [%s]", adapter, i)
            current_adapter_group_size += 1
            try:
                if bag_with_zero[i + 1] >= (adapter + 3):
                    logging.debug("Difference at adapter [%s] >=3", adapter)
                    logging.debug("Group size: %s", current_adapter_group_size)
                    arrangements *= self.adapter_combinations(
                        current_adapter_group_size
                    )
                    current_adapter_group_size = 0
            except IndexError:
                arrangements *= self.adapter_combinations(current_adapter_group_size)
                break

        return arrangements

    @classmethod
    def adapter_combinations(cls, n):
        if n == 0:
            return 0
        if n in (1, 2):
            return 1

        return (
            cls.adapter_combinations(n - 1)
            + cls.adapter_combinations(n - 2)
            + cls.adapter_combinations(n - 3)
        )

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
    puzzle.answer_b = bag.arrangements
