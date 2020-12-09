import logging
from collections import deque
from dataclasses import dataclass, field
from itertools import combinations

from aocd.models import Puzzle
from cached_property import cached_property

logging.basicConfig(level=logging.INFO)


@dataclass
class Cyphertext:
    stream: list
    window_size: int = 25
    window: deque = field(init=False)

    def __post_init__(self):
        self.stream = list(map(int, self.stream))
        self.window = deque(self.stream[: self.window_size], self.window_size)

    @cached_property
    def first_invalid(self):
        for n in self.stream[self.window_size :]:
            if n not in map(sum, combinations(self.window, 2)):
                return n
            self.window.append(n)

        raise ValueError("No invalid entry found.")

    @property
    def weakness(self):
        for i in range(len(self.stream), 0, -1):
            stream_index = len(self.stream) - i - 2
            contiguous_window = self.stream[stream_index:2]

            while sum(contiguous_window) <= self.first_invalid and stream_index > 0:
                if sum(contiguous_window) == self.first_invalid:
                    logging.debug("Contiguous window found: %s", contiguous_window)
                    return min(contiguous_window) + max(contiguous_window)
                stream_index -= 1
                contiguous_window.append(self.stream[stream_index])
                logging.debug("Contiguous window now: %s", contiguous_window)

        raise ValueError("No weakness found.")


if __name__ == "__main__":
    puzzle = Puzzle(year=2020, day=9)
    stream = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = Cyphertext(stream=stream).first_invalid
    puzzle.answer_b = Cyphertext(stream=stream).weakness
