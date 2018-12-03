from collections import Counter
import os
import re

from adventofcode.common.helpers import read_input


def parse_claim(claim):
    CLAIM_FORMAT = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    m = re.match(CLAIM_FORMAT, claim)
    (claim_no, start_col, start_row, width, height) = list(
        map(int, m.groups())
    )

    coordinates = list()
    for x in range(start_col, start_col + width):
        for y in range(start_row, start_row + height):
            coordinate = (x, y)
            coordinates.append(coordinate)

    return coordinates


def multiply_claimed_squares(claims):
    coordinate_counter = Counter()
    for claim in claims:
        coordinate_counter.update(parse_claim(claim))

    return len([i for i in list(coordinate_counter)
                if coordinate_counter[i] > 1])


if __name__ == '__main__':
    INPUT_DATA_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..', '..', 'input/input-day3.txt'
    )
    claims = read_input(INPUT_DATA_FILE)
    print("Problem 1:", multiply_claimed_squares(claims))
