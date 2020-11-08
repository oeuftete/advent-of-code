import pytest

from adventofcode.year2019.day1.solution import (
    fuel_requirement,
    fuel_requirements,
    recursive_fuel_requirement,
)


@pytest.mark.parametrize(
    "m,f",
    [
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583),
    ],
)
def test_fuel_requirement(m, f):
    assert fuel_requirement(m) == f


@pytest.mark.parametrize(
    "m,f",
    [
        (14, 2),
        (1969, 966),
        (100756, 50346),
    ],
)
def test_recursive_fuel_requirement(m, f):
    assert recursive_fuel_requirement(m) == f


@pytest.mark.parametrize(
    "masses, f, include_fuel",
    [
        ([12, 14, 1969, 100756], 2 + 2 + 654 + 33583, False),
        ([14, 1969, 100756], 2 + 966 + 50346, True),
    ],
)
def test_fuel_requirements(masses, f, include_fuel):
    assert fuel_requirements(masses, include_fuel=include_fuel) == f
