import pytest

from adventofcode.year2018.day11.solution import (PowerGrid)


@pytest.mark.parametrize("serial,x,y,power", [
    (8, 3, 5, 4),
    (57, 122, 79, -5),
    (39, 217, 196, 0),
    (71, 101, 153, 4),
])
def test_cell_power(serial, x, y, power):
    assert PowerGrid(serial).cell(x, y) == power


@pytest.mark.parametrize("serial, x, y, max_power", [
    (18, 33, 45, 29),
    (42, 21, 61, 30),
])
def test_max_power_square(serial, x, y, max_power):
    assert PowerGrid(serial).max_square() == (x, y, max_power)


@pytest.mark.skip(reason="Too slow!")
@pytest.mark.parametrize("serial, x, y, square_size, max_power", [
    (18, 90, 269, 16, 113),
    (42, 232, 251, 12, 119),
])
def test_max_power_any_square(serial, x, y, square_size, max_power):
    assert PowerGrid(serial).max_any_square() == (x, y, square_size, max_power)
