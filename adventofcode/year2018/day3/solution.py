from collections import Counter
import re

from aocd.models import Puzzle


def parse_claim(claim):
    CLAIM_FORMAT = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    m = re.match(CLAIM_FORMAT, claim)

    #  This probably should graduate to an object
    (claim_no, start_col, start_row, width, height) = list(map(int, m.groups()))

    coordinates = list()
    for x in range(start_col, start_col + width):
        for y in range(start_row, start_row + height):
            coordinate = (x, y)
            coordinates.append(coordinate)

    return (claim_no, coordinates)


def overlapped_squares(claims):
    coordinate_counter = Counter()
    for claim in claims:
        coordinate_counter.update(parse_claim(claim)[1])

    return [i for i in list(coordinate_counter) if coordinate_counter[i] > 1]


def unoverlapped_claim(claims):
    overlapped = set(overlapped_squares(claims))
    for claim in claims:
        (claim_no, claim_coordinates) = parse_claim(claim)
        if not (set(claim_coordinates) & overlapped):
            return claim_no


if __name__ == "__main__":
    puzzle = Puzzle(year=2018, day=3)
    claims = puzzle.input_data.split("\n")
    print("Problem 1:", len(overlapped_squares(claims)))
    print("Problem 2:", unoverlapped_claim(claims))
