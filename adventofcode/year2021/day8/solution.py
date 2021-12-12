import logging
from collections import defaultdict
from itertools import product

import attr
from aocd.models import Puzzle  # type: ignore

LOGGER = logging.getLogger("solveaocd")

SEGMENTS_USED = {
    0: [0, 1, 2, 4, 5, 6],
    1: [2, 5],
    2: [0, 2, 3, 4, 6],
    3: [0, 2, 3, 5, 6],
    4: [1, 2, 3, 5],
    5: [0, 1, 3, 5, 6],
    6: [0, 1, 3, 4, 5, 6],
    7: [0, 2, 5],
    8: [0, 1, 2, 3, 4, 5, 6],
    9: [0, 1, 2, 3, 5, 6],
}


_number_lengths = defaultdict(list)
for k, v in SEGMENTS_USED.items():
    _number_lengths[len(v)].append(k)
NUMBER_LENGTHS = dict(_number_lengths)
del _number_lengths


@attr.s
class SignalEntry:
    patterns: list[str] = attr.ib()
    outputs: list[str] = attr.ib()
    possibilities: dict[str, set[int]] = attr.ib(init=False, factory=dict)
    wire_possibilities: dict[str, set[int]] = attr.ib(init=False, factory=dict)
    lookup: dict[str, int] = attr.ib(init=False, factory=dict)

    def __attrs_post_init__(self) -> None:
        for c in "abcdefg":
            self.wire_possibilities[c] = set(range(7))

        for p in self.patterns:
            self.possibilities[p] = set(range(10))

        self.deduce()

    def deduce(self) -> None:
        #  Initial possibilities must match length
        for p in self.patterns:
            possibilities = NUMBER_LENGTHS[len(p)]
            self.possibilities[p].intersection_update(possibilities)

            #  For each pattern, the list of wire values can be any of the
            #  segments that are used for the possibilities.
            wire_possibility_set = set()
            for po in possibilities:
                wire_possibility_set.update(SEGMENTS_USED[po])

            for c in p:
                LOGGER.debug(
                    "Wire [%s] could have been [%s]...", c, self.wire_possibilities[c]
                )
                LOGGER.debug(
                    "... can now be [%s] based on pattern [%s]", wire_possibility_set, p
                )
                self.wire_possibilities[c].intersection_update(wire_possibility_set)

        valid_trees = list(
            filter(
                lambda s: len(s) == len(set(s)),
                product(*self.wire_possibilities.values()),
            )
        )

        #  Test the valid trees
        for tree in valid_trees:
            lookup = dict(zip(self.wire_possibilities.keys(), tree))
            LOGGER.debug("Checking validity of possible lookup [%s]", lookup)

            tree_ok = True

            for p in self.patterns:
                if (
                    sorted(map(lambda c, lookup=lookup: lookup[c], p))  # type: ignore
                    not in SEGMENTS_USED.values()
                ):
                    LOGGER.debug("... lookup [%s] invalid", lookup)
                    tree_ok = False
                    break

            if tree_ok:
                LOGGER.debug("... lookup [%s] matched!", lookup)
                self.lookup = lookup
                break

    @property
    def output_value(self):
        output_string = ""
        for o in self.outputs:
            segments = sorted(map(lambda c: self.lookup[c], o))
            for value, used_segments in SEGMENTS_USED.items():
                if segments == used_segments:
                    output_string += str(value)

        return int(output_string)


@attr.s
class SignalNotes:
    raw_lines: list[str] = attr.ib()
    easy_count: int = attr.ib(init=False, default=0)
    signal_entries: list[SignalEntry] = attr.ib(init=False, factory=list)

    def __attrs_post_init__(self) -> None:
        for l in self.raw_lines:
            patterns, outputs = l.split(" | ")
            self.signal_entries.append(SignalEntry(patterns.split(), outputs.split()))

            self.easy_count += len(
                list(filter(lambda v: len(v) in [2, 3, 4, 7], outputs.split()))
            )

    @property
    def output_value_sum(self) -> int:
        return sum(map(lambda se: se.output_value, self.signal_entries))


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=8)
    lines = puzzle.input_data.strip().splitlines()
    puzzle.answer_a = SignalNotes(lines).easy_count
    puzzle.answer_b = SignalNotes(lines).output_value_sum
