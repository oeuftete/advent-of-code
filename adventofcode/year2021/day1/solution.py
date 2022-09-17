import attr
from aocd.models import Puzzle  # type: ignore

from adventofcode.common.utils import list_str_to_int


@attr.s
class Sonar:
    measurements: list[int] = attr.ib(converter=list_str_to_int)

    def n_increases(self, window_size: int = 1) -> int:
        n = 0
        for i, _ in enumerate(self.measurements[window_size:], start=window_size):
            if sum(self.measurements[i - window_size + 1 : i + 1]) > sum(
                self.measurements[i - window_size : i]
            ):
                n += 1

        return n


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=1)
    measurements = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = Sonar(measurements).n_increases()
    puzzle.answer_b = Sonar(measurements).n_increases(window_size=3)
