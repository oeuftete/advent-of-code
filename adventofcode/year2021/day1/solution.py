import typing

import attr
from aocd.models import Puzzle


@attr.s
class Sonar:
    measurements: typing.List[int] = attr.ib(converter=lambda l: list(map(int, l)))

    def n_increases(self, window_size=1):
        n = 0
        for i, _ in enumerate(self.measurements[window_size:], start=window_size):
            if sum(self.measurements[i - window_size + 1: i + 1]) > sum(
                self.measurements[i - window_size: i]
            ):
                n += 1

        return n


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=1)
    measurements = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = Sonar(measurements).n_increases()
    puzzle.answer_b = Sonar(measurements).n_increases(window_size=3)
