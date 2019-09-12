from itertools import product

import pytest

from adventofcode.year2018.day3.solution import (
    overlapped_squares,
    parse_claim,
    unoverlapped_claim
)

CLAIMS = [
    '#1 @ 1,3: 4x4',
    '#2 @ 3,1: 4x4',
    '#3 @ 5,5: 2x2',
]


@pytest.mark.parametrize("claim,coordinates", [
    (CLAIMS[0], product(range(1, 5), range(3, 7))),
    (CLAIMS[1], product(range(3, 7), range(1, 5))),
    (CLAIMS[2], product(range(5, 7), range(5, 7))),
])
def test_parse_claim(claim, coordinates):
    assert sorted(parse_claim(claim)[1]) == sorted(coordinates)


@pytest.mark.parametrize("claims,area", [
    (CLAIMS, 4),
])
def test_overlapped_squares(claims, area):
    assert len(overlapped_squares(claims)) == area


@pytest.mark.parametrize("claims,id", [
    (CLAIMS, 3),
])
def test_unoverlapped_claim(claims, id):
    assert unoverlapped_claim(claims) == 3
