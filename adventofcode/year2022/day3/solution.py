from functools import cached_property
from itertools import islice
from string import ascii_letters

import attr
from aocd.models import Puzzle


@attr.s
class Rucksack:
    contents: str = attr.ib()

    @cached_property
    def compartments(self) -> tuple[str, str]:
        half = int(len(self.contents) / 2)
        return (self.contents[:half], self.contents[half:])

    @cached_property
    def common_item(self) -> str:
        return next(iter(set(self.compartments[0]) & set(self.compartments[1])))

    @cached_property
    def common_item_priority(self) -> int:
        return self.char_to_priority(self.common_item)

    @classmethod
    def char_to_priority(cls, c: str) -> int:
        return ascii_letters.index(c) + 1


def str_list_to_rucksacks(l: list[str]) -> list[Rucksack]:
    rucksacks = []
    for s in l:
        rucksacks.append(Rucksack(s))
    return rucksacks


@attr.s
class RucksackCollection:
    rucksacks: list[Rucksack] = attr.ib(converter=str_list_to_rucksacks)

    @cached_property
    def priority_sum(self) -> int:
        return sum(r.common_item_priority for r in self.rucksacks)

    @cached_property
    def rearrangement_sum(self) -> int:
        i = 0
        rsum = 0
        while len(elf_group := list(islice(self.rucksacks, i, i + 3))) > 0:
            assert len(elf_group) == 3
            i += 3
            rsum += Rucksack.char_to_priority(
                next(
                    iter(
                        set(elf_group[0].contents)
                        & set(elf_group[1].contents)
                        & set(elf_group[2].contents)
                    )
                )
            )
        return rsum


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=3)
    rc = RucksackCollection(puzzle.input_data.strip().splitlines())
    puzzle.answer_a = rc.priority_sum
    puzzle.answer_b = rc.rearrangement_sum
