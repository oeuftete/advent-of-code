import pytest

from adventofcode.year2018.day3.solution import (overlapped_squares,
                                                 parse_claim,
                                                 unoverlapped_claim)

CLAIMS = [
    '#1 @ 1,3: 4x4',
    '#2 @ 3,1: 4x4',
    '#3 @ 5,5: 2x2',
]


@pytest.mark.parametrize("claim,coordinates", [
    (CLAIMS[0], [
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 3),
        (3, 4),
        (3, 5),
        (3, 6),
        (4, 3),
        (4, 4),
        (4, 5),
        (4, 6),
    ]),
    (CLAIMS[1], [
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (6, 1),
        (6, 2),
        (6, 3),
        (6, 4),
    ]),
    (CLAIMS[2], [
        (5, 5),
        (5, 6),
        (6, 5),
        (6, 6),
    ]),
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
