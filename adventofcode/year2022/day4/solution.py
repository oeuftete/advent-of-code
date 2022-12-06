from functools import cached_property
from typing import Iterable

import attr
from aocd.models import Puzzle


@attr.s
class AssignmentValidator:
    assignment_texts: list[str] = attr.ib()
    assignment_ranges: list[tuple[Iterable[int], ...]] = attr.ib(
        factory=list, init=False
    )

    @classmethod
    def text_range_to_range(cls, r: str) -> Iterable[int]:
        (start, stop) = map(int, r.split("-"))
        return range(start, stop + 1)

    def __attrs_post_init__(self) -> None:
        for at in self.assignment_texts:
            range_tuple = tuple(map(self.text_range_to_range, at.split(",")))
            self.assignment_ranges.append(range_tuple)

    @cached_property
    def n_pairs_contained(self) -> int:
        n = 0
        for pair in self.assignment_ranges:
            overlap = set(pair[0]) & set(pair[1])
            if overlap == set(pair[0]) or overlap == set(pair[1]):
                n += 1

        return n

    @cached_property
    def n_pairs_overlap(self) -> int:
        n = 0
        for pair in self.assignment_ranges:
            overlap = set(pair[0]) & set(pair[1])
            if len(overlap) > 0:
                n += 1

        return n


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=4)
    assignment_validator = AssignmentValidator(puzzle.input_data.strip().splitlines())
    puzzle.answer_a = assignment_validator.n_pairs_contained
    puzzle.answer_b = assignment_validator.n_pairs_overlap
