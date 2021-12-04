import typing
from collections import Counter, defaultdict

import attr
from aocd.models import Puzzle  # type: ignore


@attr.s
class Diagnostic:
    measurements: typing.List[int] = attr.ib()
    counters: typing.DefaultDict[int, Counter] = attr.ib(
        init=False, factory=lambda: defaultdict(Counter)
    )
    gamma_rate: int = attr.ib(init=False)
    epsilon_rate: int = attr.ib(init=False)

    def __attrs_post_init__(self):
        for m in self.measurements:
            for i, c in enumerate(m):
                self.counters[i][c] += 1

        gamma_string = ""
        epsilon_string = ""
        for i, _ in enumerate(self.counters):
            gamma_string += self.counters[i].most_common()[0][0]
            epsilon_string += self.counters[i].most_common()[-1][0]

        self.gamma_rate = int(gamma_string, base=2)
        self.epsilon_rate = int(epsilon_string, base=2)

    @property
    def oxygen_rating(self):
        pass

    @property
    def co2_rating(self):
        pass


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=3)
    diagnostics = puzzle.input_data.strip().splitlines()
    diag = Diagnostic(diagnostics)
    puzzle.answer_a = diag.gamma_rate * diag.epsilon_rate
