import typing
from collections import Counter, defaultdict
from functools import cached_property

import attr
from aocd.models import Puzzle


@attr.s
class Diagnostic:
    measurements: list[str] = attr.ib()
    counters: typing.DefaultDict[int, Counter] = attr.ib(
        init=False, factory=lambda: defaultdict(Counter)
    )

    @cached_property
    def power_consumption(self) -> int:
        for m in self.measurements:
            for i, c in enumerate(m):
                self.counters[i][c] += 1

        gamma_string = ""
        epsilon_string = ""
        for i, _ in enumerate(self.counters):
            gamma_string += self.counters[i].most_common()[0][0]
            epsilon_string += self.counters[i].most_common()[-1][0]

        return int(gamma_string, base=2) * int(epsilon_string, base=2)

    @cached_property
    def life_support_rating(self) -> int:
        return self.oxygen_rating * self.scrubber_rating

    @cached_property
    def scrubber_rating(self) -> int:
        co2_measurements = self.measurements.copy()
        position = 0
        while len(co2_measurements) > 1:
            #  Look at the current measurements, find the least common at position i
            c = Counter(
                map(lambda m, p=position: m[p], co2_measurements)  # type: ignore[misc]
            )
            most_common = c.most_common()[0]
            least_common = c.most_common()[-1]

            least_common_c = least_common[0]
            if most_common[1] == least_common[1]:
                least_common_c = "0"

            #  filter the measurements by those with that least common item
            co2_measurements = list(
                filter(lambda m: m[position] == least_common_c, co2_measurements)
            )
            position += 1

        return int(co2_measurements[0], base=2)

    @cached_property
    def oxygen_rating(self) -> int:
        o2_measurements = self.measurements.copy()
        position = 0
        while len(o2_measurements) > 1:
            #  Look at the current measurements, find the most common at position i
            c = Counter(
                map(lambda m, p=position: m[p], o2_measurements)  # type: ignore[misc]
            )
            most_common = c.most_common()[0]
            least_common = c.most_common()[-1]

            most_common_c = most_common[0]
            if most_common[1] == least_common[1]:
                most_common_c = "1"

            #  filter the measurements by those with that most common item
            o2_measurements = list(
                filter(lambda m: m[position] == most_common_c, o2_measurements)
            )
            position += 1

        return int(o2_measurements[0], base=2)


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=3)
    diagnostics = puzzle.input_data.strip().splitlines()
    diag = Diagnostic(diagnostics)
    puzzle.answer_a = diag.power_consumption
    puzzle.answer_b = diag.life_support_rating
