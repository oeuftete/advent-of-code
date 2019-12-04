import pytest

from adventofcode.year2019.day1.solution import (fuel_requirement,
                                                 fuel_requirements)


@pytest.mark.parametrize("m,f", [
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583),
])
def test_fuel_requirement(m, f):
    assert fuel_requirement(m) == f


@pytest.mark.parametrize("masses, f", [
    ([12, 14, 1969, 100756], 2 + 2 + 654 + 33583),
])
def test_fuel_requirements(masses, f):
    assert fuel_requirements(masses) == f
