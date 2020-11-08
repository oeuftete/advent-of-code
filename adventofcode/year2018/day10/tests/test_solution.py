import pytest

from adventofcode.year2018.day10.solution import (
    data_to_sky,
    parse_point_and_vector,
)

from adventofcode.year2018.day10.tests.resources import get_test_data, get_test_result

TEST_POINTS = get_test_data()
TEST_RESULT = get_test_result()


@pytest.mark.parametrize(
    "point_s,x,y,dx,dy",
    [
        (TEST_POINTS[0], 9, 1, 0, 2),
        (TEST_POINTS[1], 7, 0, -1, 0),
        (TEST_POINTS[-1], -3, 6, 2, -1),
        (TEST_POINTS[-2], 14, 7, -2, 0),
    ],
)
def test_parse(point_s, x, y, dx, dy):
    assert parse_point_and_vector(point_s) == (x, y, dx, dy)


@pytest.mark.skip(reason="Whitespace and padding to account for")
def test_sky():
    sky = data_to_sky(TEST_POINTS)
    assert sky.dump_sky() == TEST_RESULT[0]
