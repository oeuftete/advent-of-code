import logging
import typing
from itertools import combinations

import attr
from aocd.models import Puzzle

logging.basicConfig(level=logging.INFO)


@attr.s
class Spreadsheet:
    rows: typing.List[typing.List[int]] = attr.ib(
        converter=lambda l: list(map(lambda m: list(map(int, m)), l))
    )

    def __attrs_post_init__(self):
        logging.debug(self.rows)

    @property
    def checksum(self):
        checksum = 0
        for row in self.rows:
            checksum += self.row_checksum(row)
        return checksum

    @property
    def division_checksum(self):
        checksum = 0
        for row in self.rows:
            checksum += self.row_division(row)
        return checksum

    @staticmethod
    def row_checksum(row):
        return max(row) - min(row)

    @staticmethod
    def row_division(row):
        for c in map(sorted, combinations(row, 2)):
            logging.debug("Checking combo %s", c)
            if c[1] % c[0] == 0:
                return c[1] // c[0]

        return 0


if __name__ == "__main__":
    puzzle = Puzzle(year=2017, day=2)
    rows = [r.split() for r in puzzle.input_data.strip().splitlines()]
    puzzle.answer_a = Spreadsheet(rows).checksum
    puzzle.answer_b = Spreadsheet(rows).division_checksum
