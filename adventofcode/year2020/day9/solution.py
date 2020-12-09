import logging
from collections import deque
from dataclasses import dataclass, field
from itertools import combinations

from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@dataclass
class Cyphertext:
    stream: list
    window_size: int = 25
    window: deque = field(init=False)

    def __post_init__(self):
        self.stream = list(map(int, self.stream))
        self.window = deque(self.stream[: self.window_size], self.window_size)

    @property
    def first_invalid(self):
        for n in self.stream[self.window_size :]:
            if n not in map(sum, combinations(self.window, 2)):
                return n
            self.window.append(n)

        raise ValueError("No invalid entry found.")


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=9)
    stream = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = Cyphertext(stream=stream).first_invalid
