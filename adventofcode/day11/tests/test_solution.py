import pytest

from adventofcode.day11.solution import (
    PowerGrid
)


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
