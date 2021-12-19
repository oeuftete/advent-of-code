import logging
import operator
from functools import reduce

import attr
from aocd.models import Puzzle  # type: ignore

LOGGER = logging.getLogger("solveaocd")


@attr.s
class SnailfishNumber:
    initial: str = attr.ib()
    current: str = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self.current = self.initial

    def reduce(self, n: int = None) -> None:
        i = 0
        while n is None or i < n:
            i += 1

            # Look for explosions
            if self.explode():
                continue

            # Look for splits
            #  if self.split():
            #      continue

            # We've converged
            return

    def explode(self) -> bool:
        """Try to explode, return True if exploded."""
        # Count brackets, if we get to 5 unclosed, we need to explode.
        #                matching bracket ----v
        #   - If the last char was a brace,   [x,y],z -> 0,y+z
        #   - If the last char was a comma, z,[x,y]   -> x+z,0
        bracket_level = 0
        for i, c in enumerate(self.current):
            if c == "[":
                bracket_level += 1
            elif c == "]":
                bracket_level -= 1

            if bracket_level == 5:
                LOGGER.debug("Hit bracket level 5 at index [%d]...", i)
                if self.current[i - 1] == "[":
                    replacement = f"0,{int(self.current[i+3]) + int(self.current[i+6])}"
                    self.current = (
                        self.current[:i] + replacement + self.current[i + 7 :]
                    )
                else:  # it was a comma
                    replacement = f"{int(self.current[i+1]) + int(self.current[i-2])},0"
                    self.current = (
                        self.current[: i - 2] + replacement + self.current[i + 5 :]
                    )
                return True

        return False

    #  def split(self) -> bool:
    #      """Try to split, return True if split."""
    #      return False

    def __add__(self, other) -> "SnailfishNumber":
        sn = SnailfishNumber(self.current + "," + other.current)
        sn.reduce()
        return sn


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=18)
    numbers = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = reduce(operator.add, map(SnailfishNumber, numbers))
