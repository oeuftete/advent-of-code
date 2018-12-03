import pytest

from adventofcode.day3.solution import (
    multiply_claimed_squares,
    parse_claim,
)

CLAIMS = [
    '#1 @ 1,3: 4x4',
    '#2 @ 3,1: 4x4',
    '#3 @ 5,5: 2x2',
]


@pytest.mark.parametrize("claim,coordinates", [
    (CLAIMS[0],
     [(1, 3), (1, 4), (1, 5), (1, 6),
      (2, 3), (2, 4), (2, 5), (2, 6),
      (3, 3), (3, 4), (3, 5), (3, 6),
      (4, 3), (4, 4), (4, 5), (4, 6),
      ]),
    (CLAIMS[1],
     [(3, 1), (3, 2), (3, 3), (3, 4),
      (4, 1), (4, 2), (4, 3), (4, 4),
      (5, 1), (5, 2), (5, 3), (5, 4),
      (6, 1), (6, 2), (6, 3), (6, 4),
      ]),
    (CLAIMS[2], [(5, 5), (5, 6), (6, 5), (6, 6), ]),
])
def test_parse_claim(claim, coordinates):
    assert sorted(parse_claim(claim)) == sorted(coordinates)


@pytest.mark.parametrize("claims,area", [
    (CLAIMS, 4),
])
def test_multiply_claimed_squares(claims, area):
    assert multiply_claimed_squares(claims) == area
